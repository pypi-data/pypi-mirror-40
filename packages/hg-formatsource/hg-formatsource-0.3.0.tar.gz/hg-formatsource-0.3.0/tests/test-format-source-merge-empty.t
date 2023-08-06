# Basic init

  $ code_root=`dirname $TESTDIR`

  $ cat >> json_inplace.py <<EOF
  > """ Auto-format the JSON file passed as a command-line argument and output
  > the formatted code in stdout
  > """
  > import sys
  > import json
  > with open(sys.argv[1], 'rb') as infile:
  >     obj = json.load(infile)
  > with open(sys.argv[1], 'wb') as outfile:
  >     json.dump(obj, outfile, sort_keys=True, indent=4, separators=(',', ': '))
  >     outfile.write("\n")
  > EOF

  $ cat << EOF >> $HGRCPATH
  > [extensions]
  > formatsource=${code_root}/hgext3rd/formatsource.py
  > rebase =
  > strip =
  > [format-source]
  > json = python $TESTTMP/json_format.py
  > json:mode.input = file
  > json:mode.output = pipe
  > json_inplace = python $TESTTMP/json_inplace.py
  > json_inplace:mode.input = file
  > json_inplace:mode.output = file
  > json_misconfigured = python $TESTTMP/json_inplace.py
  > json_misconfigured:mode.input = file
  > json_misconfigured:mode.output = pipe
  > [default]
  > format-source=--date '0 0'
  > [ui]
  > merge=:merge3
  > EOF
  $ HGMERGE=:merge3

  $ hg init test_repo
  $ cd test_repo

# Commit various json file

  $ cat << EOF > root-file.json
  > {"key1": 1, "key2": [5,6,7,8], "key3": ["arthur", "babar", "celeste"]}
  > EOF
  $ hg add .
  adding root-file.json
  $ hg commit --message 'initial commit'


# try to format them with a misconfigured tool

  $ hg format-source --date '0 0' json_misconfigured glob:root-file.json -m 'format the root-file'
  abort: tool 'json_misconfigured' failed to format file, no data returned: root-file.json
  [255]


XXX aborted format source left uncommited changes, it should not

  $ hg status
  M root-file.json
  $ hg revert --all
  reverting root-file.json
  $ hg log -G
  @  changeset:   0:a8315ef6b9d6
     tag:         tip
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     initial commit
  

# format them with an initially correctly configured formatter

  $ hg format-source -q --date '0 0' json_inplace glob:root-file.json -m 'format the root-file'

  $ hg export .
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID bfc8d60f05c874d573244829dcd7350b68f447c0
  # Parent  a8315ef6b9d6e3c1f132cee7648eecc442d3b369
  format the root-file
  
  diff -r a8315ef6b9d6 -r bfc8d60f05c8 .hg-format-source
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/.hg-format-source	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +{"pattern": "glob:root-file.json", "tool": "json_inplace"}
  diff -r a8315ef6b9d6 -r bfc8d60f05c8 root-file.json
  --- a/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,1 +1,14 @@
  -{"key1": 1, "key2": [5,6,7,8], "key3": ["arthur", "babar", "celeste"]}
  +{
  +    "key1": 1,
  +    "key2": [
  +        5,
  +        6,
  +        7,
  +        8
  +    ],
  +    "key3": [
  +        "arthur",
  +        "babar",
  +        "celeste"
  +    ]
  +}

# Now update the file

  $ hg up 0
  1 files updated, 0 files merged, 1 files removed, 0 files unresolved

  $ cat << EOF > root-file.json
  > {"key1": 1, "key2": [5,6,7,8], "key3": ["arthur", "babar", "celeste", "misconfigured"]}
  > EOF

  $ hg commit -qm "Update root-file.json"

# On another computer with a misconfigured formatter tool, try to merge it

  $ cat << EOF >> .hg/hgrc
  > [format-source]
  > json_inplace = python $TESTTMP/json_inplace.py
  > json_inplace:mode.input = file
  > json_inplace:mode.output = pipe
  > EOF

  $ hg merge bfc8d60f05c874d573244829dcd7350b68f447c0
  format-source: tool "'json_inplace'" returned empty string, skipping formatting for file 'root-file.json'
  format-source: tool "'json_inplace'" returned empty string, skipping formatting for file 'root-file.json'
  merging root-file.json
  format-source: tool "'json_inplace'" returned empty string, skipping formatting for file 'root-file.json'
  format-source: tool "'json_inplace'" returned empty string, skipping formatting for file 'root-file.json'
  warning: conflicts while merging root-file.json! (edit, then use 'hg resolve --mark')
  1 files updated, 0 files merged, 0 files removed, 1 files unresolved
  use 'hg resolve' to retry unresolved file merges or 'hg merge --abort' to abandon
  [1]

  $ hg diff
  diff -r 15fe4755df66 .hg-format-source
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/.hg-format-source	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +{"pattern": "glob:root-file.json", "tool": "json_inplace"}
  diff -r 15fe4755df66 root-file.json
  --- a/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,1 +1,20 @@
  +<<<<<<< working copy: 15fe4755df66 - test: Update root-file.json
   {"key1": 1, "key2": [5,6,7,8], "key3": ["arthur", "babar", "celeste", "misconfigured"]}
  +||||||| base
  +{"key1": 1, "key2": [5,6,7,8], "key3": ["arthur", "babar", "celeste"]}
  +=======
  +{
  +    "key1": 1,
  +    "key2": [
  +        5,
  +        6,
  +        7,
  +        8
  +    ],
  +    "key3": [
  +        "arthur",
  +        "babar",
  +        "celeste"
  +    ]
  +}
  +>>>>>>> merge rev:    bfc8d60f05c8 - test: format the root-file
