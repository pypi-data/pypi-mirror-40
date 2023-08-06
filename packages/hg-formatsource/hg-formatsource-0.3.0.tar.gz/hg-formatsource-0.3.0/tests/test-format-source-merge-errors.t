
Basic init

  $ code_root=`dirname $TESTDIR`

  $ cat >> json_format.py <<EOF
  > """ Auto-format the JSON file passed as a command-line argument and output
  > the formatted code in stdout
  > """
  > import sys
  > import json
  > with open(sys.argv[1], 'rb') as infile:
  >     obj = json.load(infile)
  > with sys.stdout:
  >     json.dump(obj, sys.stdout, sort_keys=True, indent=4, separators=(',', ': '))
  >     sys.stdout.write("\n")
  > EOF

  $ cat >> json_failing.py <<EOF
  > import sys
  > import json
  > with open(sys.argv[1], 'rb') as infile:
  >     obj = json.load(infile)
  > with sys.stdout:
  >     json.dump(obj, sys.stdout, sort_keys=True, indent=4, separators=(',', ': '))
  >     sys.stdout.write("\n")
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
  > json_invalid_input = python $TESTTMP/json_format.py
  > json_invalid_input:mode.input = invalid
  > json_invalid_output = python $TESTTMP/json_format.py
  > json_invalid_output:mode.input = file
  > json_invalid_output:mode.output = invalid
  > json_failing = python $TESTTMP/json_failing.py
  > json_failing:mode = pipe
  > [default]
  > format-source=--date '0 0'
  > [ui]
  > merge=:merge3
  > EOF
  $ HGMERGE=:merge3

# Test merging with an unknown tool

## Create the repo
  $ hg init merge_unknown_tool
  $ cd merge_unknown_tool

  $ cat << EOF > root-file.json
  > {"key1": 1, "key2": [5,6,7,8], "key3": ["arthur", "babar", "celeste"]}
  > EOF
  $ hg add .
  adding root-file.json
  $ hg commit --message 'initial commit'

## Format them

  $ hg format-source --date '0 0' json glob:root-file.json -m 'format the root-file'
  $ hg export
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID 9d74ea96f2aa759fb56bd6278640c3da48eceefe
  # Parent  a8315ef6b9d6e3c1f132cee7648eecc442d3b369
  format the root-file
  
  diff -r a8315ef6b9d6 -r 9d74ea96f2aa .hg-format-source
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/.hg-format-source	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +{"pattern": "glob:root-file.json", "tool": "json"}
  diff -r a8315ef6b9d6 -r 9d74ea96f2aa root-file.json
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

## Misconfigure the formatter

  $ cat << EOF >> .hg/hgrc
  > [format-source]
  > json = python $TESTTMP/json_format.py
  > json:mode.input = stdout
  > json:mode.output = file
  > EOF

## Try a merge with a bad input mode, it shouldn't abort

  $ hg up -qC 0

  $ cat << EOF > root-file.json
  > {"key1": 1, "key2": [5,6,7,8], "key3": ["arthur", "babar", "celeste", "unknown"]}
  > EOF

  $ cat << EOF >> .hg/hgrc
  > [format-source]
  > json = python $TESTTMP/json_format.py
  > json:mode.input = stdin
  > json:mode.output = file
  > EOF

  $ hg up --merge default
  format-source: could not help with the merge of root-file.json
  format-source:   running tool "json" failed: Tool json has an invalid input mode: stdin
  format-source: could not help with the merge of root-file.json
  format-source:   running tool "json" failed: Tool json has an invalid input mode: stdin
  merging root-file.json
  format-source: could not help with the merge of root-file.json
  format-source:   running tool "json" failed: Tool json has an invalid input mode: stdin
  format-source: could not help with the merge of root-file.json
  format-source:   running tool "json" failed: Tool json has an invalid input mode: stdin
  warning: conflicts while merging root-file.json! (edit, then use 'hg resolve --mark')
  1 files updated, 0 files merged, 0 files removed, 1 files unresolved
  use 'hg resolve' to retry unresolved file merges
  [1]

  $ hg diff
  diff -r 9d74ea96f2aa root-file.json
  --- a/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,3 +1,8 @@
  +<<<<<<< working copy: a8315ef6b9d6 - test: initial commit
  +{"key1": 1, "key2": [5,6,7,8], "key3": ["arthur", "babar", "celeste", "unknown"]}
  +||||||| base
  +{"key1": 1, "key2": [5,6,7,8], "key3": ["arthur", "babar", "celeste"]}
  +=======
   {
       "key1": 1,
       "key2": [
  @@ -12,3 +17,4 @@
           "celeste"
       ]
   }
  +>>>>>>> destination:  9d74ea96f2aa - test: format the root-file

  $ hg up -C .
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved

## Try a merge with a bad output mode, it shouldn't abort

  $ hg up -qC 0

  $ cat << EOF > root-file.json
  > {"key1": 1, "key2": [5,6,7,8], "key3": ["arthur", "babar", "celeste", "unknown"]}
  > EOF

  $ echo "" > .hg/hgrc
  $ cat << EOF >> .hg/hgrc
  > [format-source]
  > json = python $TESTTMP/json_format.py
  > json:mode.input = file
  > json:mode.output = stdout
  > EOF

  $ hg up --merge default
  format-source: could not help with the merge of root-file.json
  format-source:   running tool "json" failed: Tool json has an invalid output mode: stdout
  format-source: could not help with the merge of root-file.json
  format-source:   running tool "json" failed: Tool json has an invalid output mode: stdout
  merging root-file.json
  format-source: could not help with the merge of root-file.json
  format-source:   running tool "json" failed: Tool json has an invalid output mode: stdout
  format-source: could not help with the merge of root-file.json
  format-source:   running tool "json" failed: Tool json has an invalid output mode: stdout
  warning: conflicts while merging root-file.json! (edit, then use 'hg resolve --mark')
  1 files updated, 0 files merged, 0 files removed, 1 files unresolved
  use 'hg resolve' to retry unresolved file merges
  [1]

  $ hg diff
  diff -r 9d74ea96f2aa root-file.json
  --- a/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,3 +1,8 @@
  +<<<<<<< working copy: a8315ef6b9d6 - test: initial commit
  +{"key1": 1, "key2": [5,6,7,8], "key3": ["arthur", "babar", "celeste", "unknown"]}
  +||||||| base
  +{"key1": 1, "key2": [5,6,7,8], "key3": ["arthur", "babar", "celeste"]}
  +=======
   {
       "key1": 1,
       "key2": [
  @@ -12,3 +17,4 @@
           "celeste"
       ]
   }
  +>>>>>>> destination:  9d74ea96f2aa - test: format the root-file

  $ hg up -C .
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved

## Try a merge with a crashing formatter, it shouldn't abort

  $ hg up -qC 0

  $ cat << EOF > root-file.json
  > {"key1": 1, "key2": [5,6,7,8], "key3": ["arthur", "babar", "celeste", "unknown"]}
  > EOF

  $ echo "" > .hg/hgrc
  $ cat << EOF >> .hg/hgrc
  > [format-source]
  > json = python $TESTTMP/json_format.py
  > json:mode.input = pipe
  > json:mode.output = pipe
  > EOF

  $ hg up --merge default
  format-source: could not help with the merge of root-file.json
  format-source:   running tool "json" failed: json: python exited with status 1
  format-source: could not help with the merge of root-file.json
  format-source:   running tool "json" failed: json: python exited with status 1
  merging root-file.json
  format-source: could not help with the merge of root-file.json
  format-source:   running tool "json" failed: json: python exited with status 1
  format-source: could not help with the merge of root-file.json
  format-source:   running tool "json" failed: json: python exited with status 1
  warning: conflicts while merging root-file.json! (edit, then use 'hg resolve --mark')
  1 files updated, 0 files merged, 0 files removed, 1 files unresolved
  use 'hg resolve' to retry unresolved file merges
  [1]

  $ hg diff
  diff -r 9d74ea96f2aa root-file.json
  --- a/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,3 +1,8 @@
  +<<<<<<< working copy: a8315ef6b9d6 - test: initial commit
  +{"key1": 1, "key2": [5,6,7,8], "key3": ["arthur", "babar", "celeste", "unknown"]}
  +||||||| base
  +{"key1": 1, "key2": [5,6,7,8], "key3": ["arthur", "babar", "celeste"]}
  +=======
   {
       "key1": 1,
       "key2": [
  @@ -12,3 +17,4 @@
           "celeste"
       ]
   }
  +>>>>>>> destination:  9d74ea96f2aa - test: format the root-file

  $ hg up -C .
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
