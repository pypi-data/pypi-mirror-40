# Copyright 2017 Octobus <contact@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
"""help dealing with code source reformating

The extension provides a way to run code-formatting tools in a way that avoids
conflicts related to this formatting when merging/rebasing code across the
reformatting.

A new `format-source` command is provided, to apply code formatting tool on
some specific files. This information is recorded into the repository and
reused when merging. The client doing the merge needs the extension for this
logic to kick in.

Code formatting tools have to be registered in the configuration. The tool
"name" will be used to identify a specific command accross all repositories.
It is mapped to a command line that must output the formatted content on its
standard output.

For each tool a list of files affecting the result of the formatting can be
configured with the "configpaths" suboption, which is read and registered at
"hg format-source" time.  Any change in those files should trigger
reformatting.

Example::

    [format-source]
    json = python -m json.tool
    clang = clang-format -style=Mozilla
    clang:configpaths = .clang-format, .clang-format-ignore

We do not support specifying the mapping of tool name to tool command in the
repository itself for security reasons.

The formatting tools are given the input source code as stdin and should sends
back the results in stdout. This is the default behavior and it can be tweaked
by configuration:

    [format-source]
    clang = clang-format -style=Mozilla
    clang:mode = pipe

There is two possible values for the mode config knob:

    * "pipe": the source code will be provided for the formatter tool in stdin
      and the formatted code will be read from the formatter tool stdout.
    * "file": the formatter tool will be called with the filepath as argument
      and the formatted code will be read from the original file, this is
      often called inplace modification.

There is also configuration for input mode and output mode, the high-level
mode actually set both input mode and output mode to the same value if set:

Input mode values:

    * "pipe": the source code will be provided for the formatter tool in stdin.
    * "file": the formatter tool will be called with the filepath as argument.

Output mode values:

    * "pipe": the formatted code will be read from the formatter tool stdout.
    * "file": the formatted code will be read from the original file, this is
      often called inplace modification.

The code formatting information is tracked in a .hg-format-source file at the
root of the repository.

Warning: There is no special logic handling renames so moving files to a
directory not covered by the patterns used for the initial formatting will
likely fail.
"""

from __future__ import absolute_import

import json
import os
import subprocess
import tempfile

from mercurial import (
    commands,
    cmdutil,
    encoding,
    error,
    extensions,
    filemerge,
    match,
    merge,
    pycompat,
    localrepo,
    registrar,
    scmutil,
    util,
)

try:
    from mercurial.util import procutil

    procutil.shellquote
except ImportError:
    procutil = util  # procutil was not split in <= 4.5

from mercurial.i18n import _

__version__ = "0.3.0"
testedwith = "4.4 4.5 4.6 4.7 4.8"
minimumhgversion = "4.4"
buglink = "https://bitbucket.org/octobus/format-source/issues"

cmdtable = {}

if util.safehasattr(registrar, "command"):
    command = registrar.command(cmdtable)
else:  # compat with hg < 4.3
    command = cmdutil.command(cmdtable)

configtable = {}
configitem = registrar.configitem(configtable)
configitem("format-source", "^[^:]+$", default=None, generic=True)
configitem("format-source", "^[^:]+:configpaths$", default=None, generic=True)
configitem("format-source", "^[^:]*:mode$", default=None, generic=True)
configitem("format-source", "^[^:]*:mode.input$", default=None, generic=True)
configitem("format-source", "^[^:]*:mode.output$", default=None, generic=True)

file_storage_path = ".hg-format-source"

# Default settings for common formatters
DEFAULT_IO_MODE = [
    (
        "clang-format",
        "clang-format -assume-filename=$HG_FILENAME",
        (("mode", "pipe"), ("configpaths", ".clang-format, .clang-format-ignore")),
    ),
    ("black", "black -q -", (("mode", "pipe"), ("configpaths", "pyproject.toml"))),
    ("yapf", "yapf", (("mode", "pipe"), ("configpaths", ".style.yapf,setup.cfg"))),
    ("gofmt", "gofmt -e", (("mode", "pipe"),)),
    (
        "rustfmt",
        "rustfmt",
        (("mode", "pipe"), ("configpaths", "rustfmt.toml,.rustfmt.toml")),
    ),
    (
        "prettier",
        "prettier --stdin-filepath $HG_FILENAME",
        (
            ("mode", "pipe"),
            (
                "configpaths",
                ",".join(
                    [
                        ".prettierrc",
                        "prettier.yaml",
                        ".prettier.yml",
                        ".prettier.json",
                        ".prettier.toml",
                        "prettier.config.js",
                        ".prettierrc.js",
                        "package.json",
                    ]
                ),
            ),
        ),
    ),
]


class ToolAbort(error.Abort):
    """ A custom exception raised when a tool is misconfigured or crashed
    """

@command(
    "debugformatsourcechange",
    [],
    _("BASE TOP"),
)
def cmd_debug_format_change(ui, repo, base, top):
    """report files whose formatting is detected as changed in a range of
    commit
    """
    old_ctx = scmutil.revsingle(repo, base)
    new_ctx = scmutil.revsingle(repo, top)
    pattern_formatting = formatted(repo, old_ctx, new_ctx)
    files_formatting = _formattedfiles(repo, new_ctx, pattern_formatting)
    allfiles = []
    for tool, matcher in files_formatting.iteritems():
        for f in new_ctx:
            if matcher(f):
                allfiles.append((tool, f))
    allfiles.sort()
    for tool, f in allfiles:
        ui.write('[%s] %s\n' % (tool, f))

@command(
    "format-source",
    [] + commands.commitopts + commands.commitopts2,
    _("TOOL FILES+"),
)
def cmd_format_source(ui, repo, tool, *pats, **opts):
    """format source file using a registered tools

    This command run TOOL on FILES and record this information in a commit to
    help with future merge.

    The actual command run for TOOL needs to be registered in the config. See
    :hg:`help -e formatsource` for details.
    """
    if repo.getcwd():
        msg = _("format-source must be run from repository root")
        hint = _("cd %s") % repo.root
        raise error.Abort(msg, hint=hint)

    if not pats:
        raise error.Abort(_("no files specified"))

    for i, pattern in enumerate(pats):
        ptype = pattern.partition(":")[0]
        if not ptype:
            # make implicit glob patterns explicit
            ptype = "glob"
            pats[i] = "glob:%s" % pattern

    # lock the repo to make sure no content is changed
    with repo.wlock():
        # formating tool
        if " " in tool:
            raise error.Abort(_("tool name cannot contains space: '%s'") % tool)
        tool_config_files = repo.ui.configlist("format-source", "%s:configpaths" % tool)
        shell_tool_command = shell_tool(repo.ui, tool, raise_on_missing=True)
        input_mode, output_mode = iomode(repo.ui, tool)

        cmdutil.bailifchanged(repo)
        cmdutil.checkunfinished(repo, commit=True)
        wctx = repo[None]
        # files to be formatted
        matcher = rootedmatch(repo, wctx, pats)
        # perform actual formatting
        for filepath in wctx.matches(matcher):
            flags = wctx.flags(filepath)
            newcontent = run_tools(
                ui,
                repo.root,
                tool,
                shell_tool_command,
                filepath,
                filepath,
                input_mode=input_mode,
                output_mode=output_mode,
            )

            if newcontent == "":
                # check if the file itself is empty
                if open(filepath).read(1):
                    msg = _("tool %r failed to format file, no data returned: %s")
                    raise error.Abort(msg % (tool, filepath))
            # XXX we could do the whole commit in memory
            with repo.wvfs(filepath, "wb") as formatted_file:
                formatted_file.write(newcontent)
            wctx.filectx(filepath).setflags("l" in flags, "x" in flags)

        # update the storage to mark formated file as formatted
        with repo.wvfs(file_storage_path, mode="ab") as storage:
            for pattern in pats:
                # XXX if pattern was relative, we need to reroot it from the
                # repository root. For now we constrainted the command to run
                # at the root of the repository.
                data = {
                    "tool": encoding.unifromlocal(tool),
                    "pattern": encoding.unifromlocal(pattern),
                }
                if tool_config_files:
                    data["configpaths"] = [
                        encoding.unifromlocal(path) for path in tool_config_files
                    ]
                entry = json.dumps(data, sort_keys=True)
                assert "\n" not in entry
                storage.write("%s\n" % entry)

        if file_storage_path not in wctx:
            storage_matcher = scmutil.match(wctx, ["path:" + file_storage_path])
            cmdutil.add(ui, repo, storage_matcher, "", True)

        # commit the whole
        with repo.lock():
            commit_patterns = ["path:" + file_storage_path]
            commit_patterns.extend(pats)
            return commands._docommit(ui, repo, *commit_patterns, **opts)


def shell_tool(ui, tool, raise_on_missing=False):
    """ Return the shell command for the given formatter tool or abort
    """
    shell_tool = ui.config("format-source", tool)

    if not shell_tool and raise_on_missing:
        msg = _("unknow format tool: %s (no 'format-source.%s' config)")
        raise error.Abort(msg % (tool, tool))

    return shell_tool


def iomode(ui, tool):
    # Read the top-level configuration
    input_mode = None
    output_mode = None

    tool_mode = ui.config("format-source", "%s:mode" % tool)
    if tool_mode is not None:
        input_mode = tool_mode
        output_mode = tool_mode

    # Read the override, we cannot pass the default value as we support
    # Mercurial 4.4 and we need dynamic default for this
    override_input_mode = ui.config("format-source", "%s:mode.input" % tool)
    override_output_mode = ui.config("format-source", "%s:mode.output" % tool)

    if override_input_mode is not None:
        input_mode = override_input_mode

    if override_output_mode is not None:
        output_mode = override_output_mode

    return input_mode, output_mode


def system(cmd, environ=None, cwd=None, stdin=None):
    """ Reimplementation of Mercurial procutil.system (taken from Mercurial
    246b61bfdc2f) with separate streams for stdout and stderr
    """
    environ = environ.copy()
    environ = procutil.shellenviron(environ)
    if util.safehasattr(pycompat, "rapply") and util.safehasattr(
        procutil, "tonativestr"
    ):
        cwd = pycompat.rapply(procutil.tonativestr, cwd)
        environ = procutil.tonativeenv(environ)

    if stdin is None:
        stdin = subprocess.PIPE
    process = subprocess.Popen(
        procutil.quotecommand(cmd),
        shell=True,
        cwd=cwd,
        env=environ,
        close_fds=procutil.closefds,
        stdin=stdin,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    pout, perr = process.communicate()

    return process, pout, perr


def run_tools(
    ui, root, tool, cmd, filepath, filename, input_mode=None, output_mode=None
):
    """Run the a formatter tool on a specific file"""

    # Default mode values
    if input_mode is None:
        input_mode = "file"

    if output_mode is None:
        output_mode = "pipe"

    env = encoding.environ.copy()
    env["HG_FILENAME"] = filename

    format_cmd = cmd
    if input_mode == "file":
        format_cmd = "%s %s" % (cmd, procutil.shellquote(filepath))
    elif input_mode == "pipe":
        format_cmd = cmd
    else:
        errmsg = "Tool %s has an invalid input mode: %s"
        raise ToolAbort(errmsg % (tool, input_mode))

    ui.debug("running %s\n" % format_cmd)

    stdin = None
    try:
        if input_mode == "pipe":
            stdin = open(filepath)
        p, pout, perr = system(format_cmd, env, root, stdin=stdin)
    finally:
        if stdin is not None:
            stdin.close()

    if perr:
        for line in perr.splitlines():
            ui.debug("format-source: [%s] %s\n" % (tool, line))

    if p.returncode:
        errmsg = "%s: %s %s" % (
            tool,
            os.path.basename(format_cmd.split(None, 1)[0]),
            procutil.explainexit(p.returncode),
        )
        raise ToolAbort(errmsg)

    if output_mode == "pipe":
        return pout
    elif output_mode == "file":
        with open(filepath, "rb") as outfile:
            return outfile.read()
    else:
        errmsg = "Tool %s has an invalid output mode: %s"
        raise ToolAbort(errmsg % (tool, output_mode))


def touched(repo, old_ctx, new_ctx, paths):
    matcher = rootedmatch(repo, new_ctx, paths)
    if any(path in new_ctx for path in paths):
        status = old_ctx.status(other=new_ctx, match=matcher)
        return bool(status.modified or status.added)
    return False


def formatted(repo, old_ctx, new_ctx):
    """retrieve the list of formatted patterns between <old> and <new>

    return a {'tool': [patterns]} mapping
    """
    new_formatting = {}
    if touched(repo, old_ctx, new_ctx, [file_storage_path]):
        # quick and dirty line diffing
        # (the file is append only by contract)

        new_lines = set(new_ctx[file_storage_path].data().splitlines())
        old_lines = set()
        if file_storage_path in old_ctx:
            old_lines = set(old_ctx[file_storage_path].data().splitlines())
        new_lines -= old_lines
        for line in new_lines:
            entry = json.loads(line)

            def getkey(key):
                return encoding.unitolocal(entry[key])

            new_formatting.setdefault(getkey("tool"), set()).add(getkey("pattern"))
    if file_storage_path in old_ctx:
        for line in old_ctx[file_storage_path].data().splitlines():
            entry = json.loads(line)
            if not entry.get("configpaths"):
                continue
            configpaths = [encoding.unitolocal(path) for path in entry["configpaths"]]

            def getkey(key):
                return encoding.unitolocal(entry[key])

            if touched(repo, old_ctx, new_ctx, configpaths):
                new_formatting.setdefault(getkey("tool"), set()).add(getkey("pattern"))
    return new_formatting


def allformatted(repo, local, other, ancestor):
    """return a mapping of formatting needed for all involved changeset
    """

    cachekey = (local.node, other.node(), ancestor.node())
    cached = getattr(repo, "_formatting_cache", {}).get(cachekey)

    if cached is not None:
        return cached

    local_formating = formatted(repo, ancestor, local)
    other_formating = formatted(repo, ancestor, other)
    full_formating = local_formating.copy()
    for key, value in other_formating.iteritems():
        if key in local_formating:
            value = value | local_formating[key]
        full_formating[key] = value

    all = [
        (local, local_formating),
        (other, other_formating),
        (ancestor, full_formating),
    ]
    final = []
    for ctx, formatting in all:
        filesformatting = _formattedfiles(repo, ctx, formatting)
        final.append(filesformatting)

    final = tuple(final)
    getattr(repo, "_formatting_cache", {})[cachekey] = final
    return final

def _formattedfiles(repo, ctx, patterns_formatting):
    """Turn patterns based formatting information into concrete files"""
    files_formatting = {}
    for tool, patterns in patterns_formatting.iteritems():
        files_formatting[tool] = rootedmatch(repo, ctx, patterns)
    return files_formatting


def rootedmatch(repo, ctx, patterns):
    """match patterns agains the root of a repository"""
    # rework of basectx.match to ignore current working directory
    orig = match.match
    try:
        def _rootedmatch(root, cwd, *args, **kwargs):
            return orig(root, root, *args, **kwargs)
        match.match = _rootedmatch

        # Only a case insensitive filesystem needs magic to translate user input
        # to actual case in the filesystem.
        icasefs = not util.fscasesensitive(repo.root)
        if util.safehasattr(match, "icasefsmatcher"):  # < hg 4.3
            if icasefs:
                return match.icasefsmatcher(
                    repo.root,
                    repo.root,
                    patterns,
                    default="glob",
                    auditor=repo.auditor,
                    ctx=ctx,
                )
            else:
                return match.match(
                    repo.root,
                    repo.root,
                    patterns,
                    default="glob",
                    auditor=repo.auditor,
                    ctx=ctx,
                )
        else:
            return match.match(
                repo.root,
                repo.root,
                patterns,
                default="glob",
                auditor=repo.auditor,
                ctx=ctx,
                icasefs=icasefs,
            )
    finally:
        match.match = orig


def apply_formating(repo, formatting, fctx):
    """apply formatting to a file context (if applicable)

    only called during merging situation"""
    data = None
    for tool, matcher in sorted(formatting.items()):
        # matches?
        if matcher(fctx.path()):
            if data is None:
                data = fctx.data()

            shell_tool_command = shell_tool(repo.ui, tool, raise_on_missing=False)
            if not shell_tool_command:
                msg = _(
                    "format-source, no command defined for '%s',"
                    " skipping formating: '%s'\n"
                )
                msg %= (tool, fctx.path())
                repo.ui.warn(msg)
                continue

            input_mode, output_mode = iomode(repo.ui, tool)

            with tempfile.NamedTemporaryFile(mode="wb") as f:
                olddata = data
                f.write(data)
                f.flush()
                try:
                    data = run_tools(
                        repo.ui,
                        repo.root,
                        tool,
                        shell_tool_command,
                        f.name,
                        fctx.path(),
                        input_mode=input_mode,
                        output_mode=output_mode,
                    )
                except ToolAbort as exc:
                    # Do not abort in those cases
                    msg = _(
                        "format-source: could not help with the merge of %s\n"
                        'format-source:   running tool "%s" failed: %s\n'
                    )
                    msg %= (fctx._path, tool, exc)
                    repo.ui.warn(msg)

                if olddata and not data:
                    msg = _(
                        'format-source: tool "%r" returned empty string,'
                        " skipping formatting for file %r\n"
                    )
                    msg %= (tool, fctx.path())

                    repo.ui.warn(msg)
                    data = None

    if data is not None:
        fctx.data = lambda: data


def wrap_filemerge44(
    origfunc, premerge, repo, wctx, mynode, orig, fcd, fco, fca, *args, **kwargs
):
    """wrap the file merge logic to apply formatting on files that needs them"""
    _update_filemerge_content(repo, fcd, fco, fca)
    return origfunc(premerge, repo, wctx, mynode, orig, fcd, fco, fca, *args, **kwargs)


def wrap_filemerge43(
    origfunc, premerge, repo, mynode, orig, fcd, fco, fca, *args, **kwargs
):
    """wrap the file merge logic to apply formatting on files that needs them"""
    _update_filemerge_content(repo, fcd, fco, fca)
    return origfunc(premerge, repo, mynode, orig, fcd, fco, fca, *args, **kwargs)


def _update_filemerge_content(repo, fcd, fco, fca):
    if fcd.isabsent() or fco.isabsent() or fca.isabsent():
        return
    local = fcd._changectx
    other = fco._changectx
    ances = fca._changectx
    all = allformatted(repo, local, other, ances)
    local_formating, other_formating, full_formating = all
    apply_formating(repo, local_formating, fco)
    apply_formating(repo, other_formating, fcd)
    apply_formating(repo, full_formating, fca)

    if "data" in vars(fcd):  # XXX hacky way to check if data overwritten
        file_path = repo.wvfs.join(fcd.path())
        with open(file_path, "wb") as local_file:
            local_file.write(fcd.data())


def wrap_update(orig, repo, *args, **kwargs):
    """install the formatting cache"""
    repo._formatting_cache = {}
    try:
        return orig(repo, *args, **kwargs)
    finally:
        del repo._formatting_cache


def uisetup(ui):
    pre44hg = filemerge._filemerge.__code__.co_argcount < 9
    if pre44hg:
        extensions.wrapfunction(filemerge, "_filemerge", wrap_filemerge43)
    else:
        extensions.wrapfunction(filemerge, "_filemerge", wrap_filemerge44)
    extensions.wrapfunction(merge, "update", wrap_update)


def reposetup(ui, repo):
    if not isinstance(repo, localrepo.localrepository):
        return

    # Update the config in reposetup as the ui object passed in uisetup is
    # copied without the config set by ui.setupconfig
    for tool_name, tool_command, tool_config in DEFAULT_IO_MODE:
        # Don't overwrite the user-defined config
        if ui.hasconfig("format-source", tool_name):
            continue

        ui.setconfig("format-source", tool_name, tool_command)

        for config_name, config_value in tool_config:
            config_key = "%s:%s" % (tool_name, config_name)
            ui.setconfig("format-source", config_key, config_value)
