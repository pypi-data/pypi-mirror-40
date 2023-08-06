This test file is checking handling of various fileset patterns,

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

  $ cat << EOF >> $HGRCPATH
  > [extensions]
  > formatsource=${code_root}/hgext3rd/formatsource.py
  > rebase =
  > strip =
  > [format-source]
  > json = python $TESTTMP/json_format.py
  > json:mode.input = file
  > json:mode.output = pipe
  > [default]
  > format-source=--date '0 0'
  > [ui]
  > merge=:merge3
  > EOF
  $ HGMERGE=:merge3

  $ hg init test_repo
  $ cd test_repo

Commit various json file

  $ cat << EOF > root-file.json
  > {"key1": 1, "key2": [5,6,7,8], "key3": ["arthur", "babar", "celeste"]}
  > EOF
  $ mkdir dir-1
  $ cat << EOF > dir-1/file-1.json
  > {"key1": [42,53,78], "key2": [9,3,8,1], "key3": ["London", "Paris", "Tokyo"]}
  > EOF
  $ cat << EOF > dir-1/file-2.json
  > {"key1": 1, "key2": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], "key3": [54]}
  > EOF
  $ mkdir dir-2
  $ cat << EOF > dir-2/file-1.json
  > {"key1": [44,50,82], "key2": [4, 8, -4, 5], "key3": ["Asia", "Europe"]}
  > EOF
  $ cat << EOF > dir-2/file-2.json
  > {"key1": 6,
  > "key2": [3, 5, -2, 3, 4, 11, 10, -4, 8, 9],
  > "key3": [898, 32543, 2342]}
  > EOF
  $ cat << EOF > "dir-2/file 3.json"
  > {"key1": "hello", "key2": [3, 1, 8, -1, 19, 2], "key3": "babar"}
  > EOF
  $ hg add .
  adding dir-1/file-1.json
  adding dir-1/file-2.json
  adding dir-2/file 3.json
  adding dir-2/file-1.json
  adding dir-2/file-2.json
  adding root-file.json
  $ hg commit --message 'root-1: initial commit'

Formating using simple pattern
------------------------------

  $ hg format-source --date '0 0' json glob:root-file.json -m 'simple-1: format root file'
  $ hg export
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID 1c6aa0773267d8fe606ec36a4c033285b3149789
  # Parent  5adb80f62d483760827249087835977067863e56
  simple-1: format root file
  
  diff -r 5adb80f62d48 -r 1c6aa0773267 .hg-format-source
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/.hg-format-source	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +{"pattern": "glob:root-file.json", "tool": "json"}
  diff -r 5adb80f62d48 -r 1c6aa0773267 root-file.json
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
  $ hg format-source --date '0 0' json 'glob:dir-1/**' -m 'simple-2: format dir1 as a whole'
  $ hg export
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID b01033143f6e0081b54a36f30740352209a04ad3
  # Parent  1c6aa0773267d8fe606ec36a4c033285b3149789
  simple-2: format dir1 as a whole
  
  diff -r 1c6aa0773267 -r b01033143f6e .hg-format-source
  --- a/.hg-format-source	Thu Jan 01 00:00:00 1970 +0000
  +++ b/.hg-format-source	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,1 +1,2 @@
   {"pattern": "glob:root-file.json", "tool": "json"}
  +{"pattern": "glob:dir-1/**", "tool": "json"}
  diff -r 1c6aa0773267 -r b01033143f6e dir-1/file-1.json
  --- a/dir-1/file-1.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/dir-1/file-1.json	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,1 +1,18 @@
  -{"key1": [42,53,78], "key2": [9,3,8,1], "key3": ["London", "Paris", "Tokyo"]}
  +{
  +    "key1": [
  +        42,
  +        53,
  +        78
  +    ],
  +    "key2": [
  +        9,
  +        3,
  +        8,
  +        1
  +    ],
  +    "key3": [
  +        "London",
  +        "Paris",
  +        "Tokyo"
  +    ]
  +}
  diff -r 1c6aa0773267 -r b01033143f6e dir-1/file-2.json
  --- a/dir-1/file-2.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/dir-1/file-2.json	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,1 +1,18 @@
  -{"key1": 1, "key2": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], "key3": [54]}
  +{
  +    "key1": 1,
  +    "key2": [
  +        0,
  +        1,
  +        2,
  +        3,
  +        4,
  +        5,
  +        6,
  +        7,
  +        8,
  +        9
  +    ],
  +    "key3": [
  +        54
  +    ]
  +}
  $ hg format-source --date '0 0' json glob:dir-2/file-1.json "glob:dir-2/file 3.json" -m 'simple-3: format some dir2 with explicite pattern'
  $ hg export
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID 40997ee0defc96accac98eebbf2039ed9ce35519
  # Parent  b01033143f6e0081b54a36f30740352209a04ad3
  simple-3: format some dir2 with explicite pattern
  
  diff -r b01033143f6e -r 40997ee0defc .hg-format-source
  --- a/.hg-format-source	Thu Jan 01 00:00:00 1970 +0000
  +++ b/.hg-format-source	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,2 +1,4 @@
   {"pattern": "glob:root-file.json", "tool": "json"}
   {"pattern": "glob:dir-1/**", "tool": "json"}
  +{"pattern": "glob:dir-2/file-1.json", "tool": "json"}
  +{"pattern": "glob:dir-2/file 3.json", "tool": "json"}
  diff -r b01033143f6e -r 40997ee0defc dir-2/file 3.json
  --- a/dir-2/file 3.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/dir-2/file 3.json	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,1 +1,12 @@
  -{"key1": "hello", "key2": [3, 1, 8, -1, 19, 2], "key3": "babar"}
  +{
  +    "key1": "hello",
  +    "key2": [
  +        3,
  +        1,
  +        8,
  +        -1,
  +        19,
  +        2
  +    ],
  +    "key3": "babar"
  +}
  diff -r b01033143f6e -r 40997ee0defc dir-2/file-1.json
  --- a/dir-2/file-1.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/dir-2/file-1.json	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,1 +1,17 @@
  -{"key1": [44,50,82], "key2": [4, 8, -4, 5], "key3": ["Asia", "Europe"]}
  +{
  +    "key1": [
  +        44,
  +        50,
  +        82
  +    ],
  +    "key2": [
  +        4,
  +        8,
  +        -4,
  +        5
  +    ],
  +    "key3": [
  +        "Asia",
  +        "Europe"
  +    ]
  +}
  $ hg log -G
  @  changeset:   3:40997ee0defc
  |  tag:         tip
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     simple-3: format some dir2 with explicite pattern
  |
  o  changeset:   2:b01033143f6e
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     simple-2: format dir1 as a whole
  |
  o  changeset:   1:1c6aa0773267
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     simple-1: format root file
  |
  o  changeset:   0:5adb80f62d48
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     root-1: initial commit
  

Check the actual matching

  $ hg up null
  0 files updated, 0 files merged, 7 files removed, 0 files unresolved
  $ cd $TESTTMP
  $ hg -R test_repo status -I "glob:test_repo/**/*.json" --rev 'desc("root-1")' --rev 'desc("simple-1")'
  M root-file.json
  $ hg -R test_repo debugformatsourcechange 'desc("root-1")' 'desc("simple-1")'
  [json] root-file.json
  $ hg -R test_repo status -I "glob:test_repo/**/*.json" --rev 'desc("root-1")' --rev 'desc("simple-3")'
  M dir-1/file-1.json
  M dir-1/file-2.json
  M dir-2/file 3.json
  M dir-2/file-1.json
  M root-file.json
  $ hg -R test_repo debugformatsourcechange 'desc("root-1")' 'desc("simple-3")'
  [json] dir-1/file-1.json
  [json] dir-1/file-2.json
  [json] dir-2/file 3.json
  [json] dir-2/file-1.json
  [json] root-file.json
  $ hg -R test_repo status -I "glob:test_repo/**/*.json" --rev 'desc("simple-1")' --rev 'desc("simple-3")'
  M dir-1/file-1.json
  M dir-1/file-2.json
  M dir-2/file 3.json
  M dir-2/file-1.json
  $ hg -R test_repo debugformatsourcechange 'desc("simple-1")' 'desc("simple-3")'
  [json] dir-1/file-1.json
  [json] dir-1/file-2.json
  [json] dir-2/file 3.json
  [json] dir-2/file-1.json
  $ hg -R test_repo status -I "glob:test_repo/**/*.json" --rev 'desc("simple-1")' --rev 'desc("simple-2")'
  M dir-1/file-1.json
  M dir-1/file-2.json
  $ hg -R test_repo debugformatsourcechange 'desc("simple-1")' 'desc("simple-2")'
  [json] dir-1/file-1.json
  [json] dir-1/file-2.json
  $ hg -R test_repo status -I "glob:test_repo/**/*.json" --rev 'desc("simple-2")' --rev 'desc("simple-3")'
  M dir-2/file 3.json
  M dir-2/file-1.json
  $ hg -R test_repo debugformatsourcechange 'desc("simple-2")' 'desc("simple-3")'
  [json] dir-2/file 3.json
  [json] dir-2/file-1.json
  $ cd test_repo

Formating using advanced pattern
--------------------------------

Excluding thing in directory

  $ hg up 'desc("root-1")'
  6 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg format-source --date '0 0' json 'set: "*.json" - "dir-?/**"' -m 'complex-1: format root file'
  created new head
  $ hg status --change .
  M root-file.json
  A .hg-format-source

regexp matching

  $ hg format-source --date '0 0' json 're:[^2]+/file-2.json' -m 'complex-2: format file-2 in dir 1'
  $ hg status --change .
  M .hg-format-source
  M dir-1/file-2.json

  $ hg up null
  0 files updated, 0 files merged, 7 files removed, 0 files unresolved
  $ cd $TESTTMP
  $ hg -R test_repo status -I "glob:test_repo/**/*.json" --rev 'desc("root-1")' --rev 'desc("complex-1")'
  M root-file.json
  $ hg -R test_repo debugformatsourcechange 'desc("root-1")' 'desc("complex-1")' --traceback
  [json] root-file.json
  $ hg -R test_repo status -I "glob:test_repo/**/*.json" --rev 'desc("root-1")' --rev 'desc("complex-2")'
  M dir-1/file-2.json
  M root-file.json
  $ hg -R test_repo debugformatsourcechange 'desc("root-1")' 'desc("complex-2")'
  [json] dir-1/file-2.json
  [json] root-file.json
  $ hg -R test_repo status -I "glob:test_repo/**/*.json" --rev 'desc("complex-1")' --rev 'desc("complex-2")'
  M dir-1/file-2.json
  $ hg -R test_repo debugformatsourcechange 'desc("complex-1")' 'desc("complex-2")'
  [json] dir-1/file-2.json
  $ cd test_repo
