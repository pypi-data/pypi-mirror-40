
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
  $ hg commit --message 'initial commit'

format them (in multiple steps)

  $ hg format-source --date '0 0' json glob:root-file.json -m 'format the root-file'
  $ hg export
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID 37aedc05b31aaabe47210edf1692ab0a175479ec
  # Parent  bdc6e1fea62561308c0f00624b17fe3d25667f66
  format the root-file
  
  diff -r bdc6e1fea625 -r 37aedc05b31a .hg-format-source
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/.hg-format-source	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +{"pattern": "glob:root-file.json", "tool": "json"}
  diff -r bdc6e1fea625 -r 37aedc05b31a root-file.json
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
  $ hg format-source --date '0 0' json 'glob:dir-1/**' -m 'format dir1 as a whole'
  $ hg export
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID 7a251aee7fec4d496195baf42708da1feb1fbb1d
  # Parent  37aedc05b31aaabe47210edf1692ab0a175479ec
  format dir1 as a whole
  
  diff -r 37aedc05b31a -r 7a251aee7fec .hg-format-source
  --- a/.hg-format-source	Thu Jan 01 00:00:00 1970 +0000
  +++ b/.hg-format-source	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,1 +1,2 @@
   {"pattern": "glob:root-file.json", "tool": "json"}
  +{"pattern": "glob:dir-1/**", "tool": "json"}
  diff -r 37aedc05b31a -r 7a251aee7fec dir-1/file-1.json
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
  diff -r 37aedc05b31a -r 7a251aee7fec dir-1/file-2.json
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
  $ hg format-source --date '0 0' json glob:dir-2/file-1.json "glob:dir-2/file 3.json" -m 'format some dir2 with explicite pattern'
  $ hg export
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID 7e4070817d0b27dae5c40d99799adeca684a5e4c
  # Parent  7a251aee7fec4d496195baf42708da1feb1fbb1d
  format some dir2 with explicite pattern
  
  diff -r 7a251aee7fec -r 7e4070817d0b .hg-format-source
  --- a/.hg-format-source	Thu Jan 01 00:00:00 1970 +0000
  +++ b/.hg-format-source	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,2 +1,4 @@
   {"pattern": "glob:root-file.json", "tool": "json"}
   {"pattern": "glob:dir-1/**", "tool": "json"}
  +{"pattern": "glob:dir-2/file-1.json", "tool": "json"}
  +{"pattern": "glob:dir-2/file 3.json", "tool": "json"}
  diff -r 7a251aee7fec -r 7e4070817d0b dir-2/file 3.json
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
  diff -r 7a251aee7fec -r 7e4070817d0b dir-2/file-1.json
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
  @  changeset:   3:7e4070817d0b
  |  tag:         tip
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     format some dir2 with explicite pattern
  |
  o  changeset:   2:7a251aee7fec
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     format dir1 as a whole
  |
  o  changeset:   1:37aedc05b31a
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     format the root-file
  |
  o  changeset:   0:bdc6e1fea625
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     initial commit
  

Test merging
============

Simple case, the root file

  $ hg up 0
  5 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ cat << EOF > root-file.json
  > {"key1": 1, "key2": [5,6,7,8], "key3": ["arthur", "babar", "celeste", "pomme"]}
  > EOF
  $ hg branch B_A
  marked working directory as branch B_A
  (branches are permanent and global, did you want a bookmark?)
  $ hg ci -m 'update root-file'
  $ hg merge 1
  merging root-file.json
  1 files updated, 1 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)
  $ hg diff -r 'p1()'
  diff -r 609ee0b152e0 .hg-format-source
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/.hg-format-source	* (glob)
  @@ -0,0 +1,1 @@
  +{"pattern": "glob:root-file.json", "tool": "json"}
  diff -r 609ee0b152e0 root-file.json
  --- a/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/root-file.json	* (glob)
  @@ -1,1 +1,15 @@
  -{"key1": 1, "key2": [5,6,7,8], "key3": ["arthur", "babar", "celeste", "pomme"]}
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
  +        "celeste",
  +        "pomme"
  +    ]
  +}
  $ hg diff -r 'p2()'
  diff -r 37aedc05b31a root-file.json
  --- a/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/root-file.json	* (glob)
  @@ -9,6 +9,7 @@
       "key3": [
           "arthur",
           "babar",
  -        "celeste"
  +        "celeste",
  +        "pomme"
       ]
   }

Same from the other direction

  $ hg up -C 1
  2 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg merge B_A
  merging root-file.json
  0 files updated, 1 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)
  $ hg diff -r 'p1()'
  diff -r 37aedc05b31a root-file.json
  --- a/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/root-file.json	* (glob)
  @@ -9,6 +9,7 @@
       "key3": [
           "arthur",
           "babar",
  -        "celeste"
  +        "celeste",
  +        "pomme"
       ]
   }
  $ hg diff -r 'p2()'
  diff -r 609ee0b152e0 .hg-format-source
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/.hg-format-source	* (glob)
  @@ -0,0 +1,1 @@
  +{"pattern": "glob:root-file.json", "tool": "json"}
  diff -r 609ee0b152e0 root-file.json
  --- a/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/root-file.json	* (glob)
  @@ -1,1 +1,15 @@
  -{"key1": 1, "key2": [5,6,7,8], "key3": ["arthur", "babar", "celeste", "pomme"]}
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
  +        "celeste",
  +        "pomme"
  +    ]
  +}

Merging change on both side:

  $ hg up -C 1
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg branch B_B
  marked working directory as branch B_B

  $ echo '{"key1": 4, "key2": [5,6,7,8], "key3": ["arthur", "babar", "celeste"]}' | python -m json.tool > root-file.json
  $ hg ci -m 'update key 1'
  $ hg merge B_A
  merging root-file.json
  0 files updated, 1 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)
  $ hg diff -r 'p1()'
  diff -r ade957fdb911 root-file.json
  --- a/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/root-file.json	* (glob)
  @@ -9,6 +9,7 @@
       "key3": [
           "arthur",
           "babar",
  -        "celeste"
  +        "celeste",
  +        "pomme"
       ]
   }
  $ hg diff -r 'p2()'
  diff -r 609ee0b152e0 .hg-format-source
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/.hg-format-source	* (glob)
  @@ -0,0 +1,1 @@
  +{"pattern": "glob:root-file.json", "tool": "json"}
  diff -r 609ee0b152e0 root-file.json
  --- a/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/root-file.json	* (glob)
  @@ -1,1 +1,15 @@
  -{"key1": 1, "key2": [5,6,7,8], "key3": ["arthur", "babar", "celeste", "pomme"]}
  +{
  +    "key1": 4,
  +    "key2": [
  +        5,
  +        6,
  +        7,
  +        8
  +    ],
  +    "key3": [
  +        "arthur",
  +        "babar",
  +        "celeste",
  +        "pomme"
  +    ]
  +}

Merging with conflict

  $ hg up -C B_B
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved

  $ echo '{"key1": 4, "key2": [5,6,7,8], "key3": ["arthur", "babar", "celeste", "Flore"]}' | python -m json.tool > root-file.json
  $ hg ci -m 'conflicting update'
  $ hg merge B_A
  merging root-file.json
  warning: conflicts while merging root-file.json! (edit, then use 'hg resolve --mark')
  0 files updated, 0 files merged, 0 files removed, 1 files unresolved
  use 'hg resolve' to retry unresolved file merges or 'hg merge --abort' to abandon (hg45 !)
  use 'hg resolve' to retry unresolved file merges or 'hg update -C .' to abandon (no-hg45 !)
  [1]
  $ hg resolve -l
  U root-file.json
  $ hg diff -r 'p1()'
  diff -r ca3f6acf64a5 root-file.json
  --- a/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/root-file.json	* (glob)
  @@ -9,7 +9,14 @@
       "key3": [
           "arthur",
           "babar",
  +<<<<<<< working copy: ca3f6acf64a5 B_B - test: conflicting update
           "celeste",
           "Flore"
  +||||||| base
  +        "celeste"
  +=======
  +        "celeste",
  +        "pomme"
  +>>>>>>> merge rev:    609ee0b152e0 B_A - test: update root-file
       ]
   }
  $ hg diff -r 'p2()'
  diff -r 609ee0b152e0 .hg-format-source
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/.hg-format-source	* (glob)
  @@ -0,0 +1,1 @@
  +{"pattern": "glob:root-file.json", "tool": "json"}
  diff -r 609ee0b152e0 root-file.json
  --- a/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/root-file.json	* (glob)
  @@ -1,1 +1,22 @@
  -{"key1": 1, "key2": [5,6,7,8], "key3": ["arthur", "babar", "celeste", "pomme"]}
  +{
  +    "key1": 4,
  +    "key2": [
  +        5,
  +        6,
  +        7,
  +        8
  +    ],
  +    "key3": [
  +        "arthur",
  +        "babar",
  +<<<<<<< working copy: ca3f6acf64a5 B_B - test: conflicting update
  +        "celeste",
  +        "Flore"
  +||||||| base
  +        "celeste"
  +=======
  +        "celeste",
  +        "pomme"
  +>>>>>>> merge rev:    609ee0b152e0 B_A - test: update root-file
  +    ]
  +}

Test merge with no reformating needed
-------------------------------------

  $ hg up -C B_B
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg merge default
  5 files updated, 0 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)
  $ hg diff -r 'p2()'
  diff -r 7e4070817d0b root-file.json
  --- a/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/root-file.json	* (glob)
  @@ -1,5 +1,5 @@
   {
  -    "key1": 1,
  +    "key1": 4,
       "key2": [
           5,
           6,
  @@ -9,6 +9,7 @@
       "key3": [
           "arthur",
           "babar",
  -        "celeste"
  +        "celeste",
  +        "Flore"
       ]
   }

Test rebase
-----------

  $ hg up -C B_A
  5 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ hg rebase -d default
  rebasing 4:609ee0b152e0 "update root-file"
  merging root-file.json
  saved backup bundle to $TESTTMP/test_repo/.hg/strip-backup/609ee0b152e0-a6010e72-rebase.hg (glob)
  $ hg export
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID db9ac9e49e2df47a97f7722fe6d1ff3724a17603
  # Parent  7e4070817d0b27dae5c40d99799adeca684a5e4c
  update root-file
  
  diff -r 7e4070817d0b -r db9ac9e49e2d root-file.json
  --- a/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  @@ -9,6 +9,7 @@
       "key3": [
           "arthur",
           "babar",
  -        "celeste"
  +        "celeste",
  +        "pomme"
       ]
   }
  $ hg log -G
  @  changeset:   6:db9ac9e49e2d
  |  tag:         tip
  |  parent:      3:7e4070817d0b
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     update root-file
  |
  | o  changeset:   5:ca3f6acf64a5
  | |  branch:      B_B
  | |  user:        test
  | |  date:        Thu Jan 01 00:00:00 1970 +0000
  | |  summary:     conflicting update
  | |
  | o  changeset:   4:ade957fdb911
  | |  branch:      B_B
  | |  parent:      1:37aedc05b31a
  | |  user:        test
  | |  date:        Thu Jan 01 00:00:00 1970 +0000
  | |  summary:     update key 1
  | |
  o |  changeset:   3:7e4070817d0b
  | |  user:        test
  | |  date:        Thu Jan 01 00:00:00 1970 +0000
  | |  summary:     format some dir2 with explicite pattern
  | |
  o |  changeset:   2:7a251aee7fec
  |/   user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    summary:     format dir1 as a whole
  |
  o  changeset:   1:37aedc05b31a
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     format the root-file
  |
  o  changeset:   0:bdc6e1fea625
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     initial commit
  

Test update
-----------

  $ hg up -C 0
  5 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ cat << EOF > root-file.json
  > {"key1": 1, "key2": [4,6,7,8], "key3": ["arthur", "babar", "celeste"]}
  > EOF
  $ hg diff
  diff -r bdc6e1fea625 root-file.json
  --- a/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/root-file.json	* (glob)
  @@ -1,1 +1,1 @@
  -{"key1": 1, "key2": [5,6,7,8], "key3": ["arthur", "babar", "celeste"]}
  +{"key1": 1, "key2": [4,6,7,8], "key3": ["arthur", "babar", "celeste"]}
  $ hg up --merge
  merging root-file.json
  5 files updated, 1 files merged, 0 files removed, 0 files unresolved
  $ hg diff
  diff -r db9ac9e49e2d root-file.json
  --- a/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/root-file.json	* (glob)
  @@ -1,7 +1,7 @@
   {
       "key1": 1,
       "key2": [
  -        5,
  +        4,
           6,
           7,
           8


Test multiple change to multiple file accross multiple revisions
----------------------------------------------------------------

modify one side

  $ hg up -C default
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ echo '{"key1": [42,53,76], "key2": [9,3,8,1], "key3": ["London", "Paris", "Tokyo"]}' | python -m json.tool > dir-1/file-1.json
  $ hg diff
  diff -r db9ac9e49e2d dir-1/file-1.json
  --- a/dir-1/file-1.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/dir-1/file-1.json	* (glob)
  @@ -2,7 +2,7 @@
       "key1": [
           42,
           53,
  -        78
  +        76
       ],
       "key2": [
           9,
  $ hg ci -m 'update d1f1'
  $ echo '{"key1": 4, "key2": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], "key3": [54]}' | python -m json.tool > dir-1/file-2.json
  $ echo '{"key1": [44,50,86], "key2": [4, 8, -4, 5], "key3": ["Asia", "Europe", "Oceania"]}' | python -m json.tool > dir-2/file-1.json
  $ hg diff
  diff -r fd4a3a3a3955 dir-1/file-2.json
  --- a/dir-1/file-2.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/dir-1/file-2.json	* (glob)
  @@ -1,5 +1,5 @@
   {
  -    "key1": 1,
  +    "key1": 4,
       "key2": [
           0,
           1,
  diff -r fd4a3a3a3955 dir-2/file-1.json
  --- a/dir-2/file-1.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/dir-2/file-1.json	* (glob)
  @@ -2,7 +2,7 @@
       "key1": [
           44,
           50,
  -        82
  +        86
       ],
       "key2": [
           4,
  @@ -12,6 +12,7 @@
       ],
       "key3": [
           "Asia",
  -        "Europe"
  +        "Europe",
  +        "Oceania"
       ]
   }
  $ hg ci -m 'update d1f2 and d2f1'

modify the other side

  $ hg up -C B_B
  6 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ echo '{"key1": 1337, "key2": [5,6,7,8], "key3": ["arthur", "babar", "celeste"]}' | python -m json.tool > root-file.json
  $ echo '{"key1": 4, "key2": [0, 1, 3, 3, 7, 5, 9, 7, 8, 9], "key3": [54]}' > dir-1/file-2.json
  $ hg diff
  diff -r ca3f6acf64a5 dir-1/file-2.json
  --- a/dir-1/file-2.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/dir-1/file-2.json	* (glob)
  @@ -1,1 +1,1 @@
  -{"key1": 1, "key2": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], "key3": [54]}
  +{"key1": 4, "key2": [0, 1, 3, 3, 7, 5, 9, 7, 8, 9], "key3": [54]}
  diff -r ca3f6acf64a5 root-file.json
  --- a/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/root-file.json	* (glob)
  @@ -1,5 +1,5 @@
   {
  -    "key1": 4,
  +    "key1": 1337,
       "key2": [
           5,
           6,
  @@ -9,7 +9,6 @@
       "key3": [
           "arthur",
           "babar",
  -        "celeste",
  -        "Flore"
  +        "celeste"
       ]
   }
  $ hg ci -m 'update root-file and d1f2'
  $ cat << EOF > dir-2/file-2.json
  > {"key1": 6,
  > "key2": [3, 5, -2, 3, 4, 11, 10, -4, 8, 9],
  > "key3": [898, 32543, 2336]}
  > EOF
  $ echo '{"key1": "hello", "key2": [6, 1, 8, -1, 19, 2], "key3": "Babar"}' > "dir-2/file 3.json"
  $ hg diff
  diff -r 039f5de9b75e dir-2/file 3.json
  --- a/dir-2/file 3.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/dir-2/file 3.json	* (glob)
  @@ -1,1 +1,1 @@
  -{"key1": "hello", "key2": [3, 1, 8, -1, 19, 2], "key3": "babar"}
  +{"key1": "hello", "key2": [6, 1, 8, -1, 19, 2], "key3": "Babar"}
  diff -r 039f5de9b75e dir-2/file-2.json
  --- a/dir-2/file-2.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/dir-2/file-2.json	* (glob)
  @@ -1,3 +1,3 @@
   {"key1": 6,
   "key2": [3, 5, -2, 3, 4, 11, 10, -4, 8, 9],
  -"key3": [898, 32543, 2342]}
  +"key3": [898, 32543, 2336]}
  $ hg ci -m 'update d2f2 and d2f3'

Check output before leaping

  $ hg log -Gp -r 'sort(all(), "topo")'
  @  changeset:   10:7414847d3de4
  |  branch:      B_B
  |  tag:         tip
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     update d2f2 and d2f3
  |
  |  diff -r 039f5de9b75e -r 7414847d3de4 dir-2/file 3.json
  |  --- a/dir-2/file 3.json	Thu Jan 01 00:00:00 1970 +0000
  |  +++ b/dir-2/file 3.json	Thu Jan 01 00:00:00 1970 +0000
  |  @@ -1,1 +1,1 @@
  |  -{"key1": "hello", "key2": [3, 1, 8, -1, 19, 2], "key3": "babar"}
  |  +{"key1": "hello", "key2": [6, 1, 8, -1, 19, 2], "key3": "Babar"}
  |  diff -r 039f5de9b75e -r 7414847d3de4 dir-2/file-2.json
  |  --- a/dir-2/file-2.json	Thu Jan 01 00:00:00 1970 +0000
  |  +++ b/dir-2/file-2.json	Thu Jan 01 00:00:00 1970 +0000
  |  @@ -1,3 +1,3 @@
  |   {"key1": 6,
  |   "key2": [3, 5, -2, 3, 4, 11, 10, -4, 8, 9],
  |  -"key3": [898, 32543, 2342]}
  |  +"key3": [898, 32543, 2336]}
  |
  o  changeset:   9:039f5de9b75e
  |  branch:      B_B
  |  parent:      5:ca3f6acf64a5
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     update root-file and d1f2
  |
  |  diff -r ca3f6acf64a5 -r 039f5de9b75e dir-1/file-2.json
  |  --- a/dir-1/file-2.json	Thu Jan 01 00:00:00 1970 +0000
  |  +++ b/dir-1/file-2.json	Thu Jan 01 00:00:00 1970 +0000
  |  @@ -1,1 +1,1 @@
  |  -{"key1": 1, "key2": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], "key3": [54]}
  |  +{"key1": 4, "key2": [0, 1, 3, 3, 7, 5, 9, 7, 8, 9], "key3": [54]}
  |  diff -r ca3f6acf64a5 -r 039f5de9b75e root-file.json
  |  --- a/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  |  +++ b/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  |  @@ -1,5 +1,5 @@
  |   {
  |  -    "key1": 4,
  |  +    "key1": 1337,
  |       "key2": [
  |           5,
  |           6,
  |  @@ -9,7 +9,6 @@
  |       "key3": [
  |           "arthur",
  |           "babar",
  |  -        "celeste",
  |  -        "Flore"
  |  +        "celeste"
  |       ]
  |   }
  |
  o  changeset:   5:ca3f6acf64a5
  |  branch:      B_B
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     conflicting update
  |
  |  diff -r ade957fdb911 -r ca3f6acf64a5 root-file.json
  |  --- a/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  |  +++ b/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  |  @@ -9,6 +9,7 @@
  |       "key3": [
  |           "arthur",
  |           "babar",
  |  -        "celeste"
  |  +        "celeste",
  |  +        "Flore"
  |       ]
  |   }
  |
  o  changeset:   4:ade957fdb911
  |  branch:      B_B
  |  parent:      1:37aedc05b31a
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     update key 1
  |
  |  diff -r 37aedc05b31a -r ade957fdb911 root-file.json
  |  --- a/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  |  +++ b/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  |  @@ -1,5 +1,5 @@
  |   {
  |  -    "key1": 1,
  |  +    "key1": 4,
  |       "key2": [
  |           5,
  |           6,
  |
  | o  changeset:   8:d5f5eb5c9a36
  | |  user:        test
  | |  date:        Thu Jan 01 00:00:00 1970 +0000
  | |  summary:     update d1f2 and d2f1
  | |
  | |  diff -r fd4a3a3a3955 -r d5f5eb5c9a36 dir-1/file-2.json
  | |  --- a/dir-1/file-2.json	Thu Jan 01 00:00:00 1970 +0000
  | |  +++ b/dir-1/file-2.json	Thu Jan 01 00:00:00 1970 +0000
  | |  @@ -1,5 +1,5 @@
  | |   {
  | |  -    "key1": 1,
  | |  +    "key1": 4,
  | |       "key2": [
  | |           0,
  | |           1,
  | |  diff -r fd4a3a3a3955 -r d5f5eb5c9a36 dir-2/file-1.json
  | |  --- a/dir-2/file-1.json	Thu Jan 01 00:00:00 1970 +0000
  | |  +++ b/dir-2/file-1.json	Thu Jan 01 00:00:00 1970 +0000
  | |  @@ -2,7 +2,7 @@
  | |       "key1": [
  | |           44,
  | |           50,
  | |  -        82
  | |  +        86
  | |       ],
  | |       "key2": [
  | |           4,
  | |  @@ -12,6 +12,7 @@
  | |       ],
  | |       "key3": [
  | |           "Asia",
  | |  -        "Europe"
  | |  +        "Europe",
  | |  +        "Oceania"
  | |       ]
  | |   }
  | |
  | o  changeset:   7:fd4a3a3a3955
  | |  user:        test
  | |  date:        Thu Jan 01 00:00:00 1970 +0000
  | |  summary:     update d1f1
  | |
  | |  diff -r db9ac9e49e2d -r fd4a3a3a3955 dir-1/file-1.json
  | |  --- a/dir-1/file-1.json	Thu Jan 01 00:00:00 1970 +0000
  | |  +++ b/dir-1/file-1.json	Thu Jan 01 00:00:00 1970 +0000
  | |  @@ -2,7 +2,7 @@
  | |       "key1": [
  | |           42,
  | |           53,
  | |  -        78
  | |  +        76
  | |       ],
  | |       "key2": [
  | |           9,
  | |
  | o  changeset:   6:db9ac9e49e2d
  | |  parent:      3:7e4070817d0b
  | |  user:        test
  | |  date:        Thu Jan 01 00:00:00 1970 +0000
  | |  summary:     update root-file
  | |
  | |  diff -r 7e4070817d0b -r db9ac9e49e2d root-file.json
  | |  --- a/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  | |  +++ b/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  | |  @@ -9,6 +9,7 @@
  | |       "key3": [
  | |           "arthur",
  | |           "babar",
  | |  -        "celeste"
  | |  +        "celeste",
  | |  +        "pomme"
  | |       ]
  | |   }
  | |
  | o  changeset:   3:7e4070817d0b
  | |  user:        test
  | |  date:        Thu Jan 01 00:00:00 1970 +0000
  | |  summary:     format some dir2 with explicite pattern
  | |
  | |  diff -r 7a251aee7fec -r 7e4070817d0b .hg-format-source
  | |  --- a/.hg-format-source	Thu Jan 01 00:00:00 1970 +0000
  | |  +++ b/.hg-format-source	Thu Jan 01 00:00:00 1970 +0000
  | |  @@ -1,2 +1,4 @@
  | |   {"pattern": "glob:root-file.json", "tool": "json"}
  | |   {"pattern": "glob:dir-1/**", "tool": "json"}
  | |  +{"pattern": "glob:dir-2/file-1.json", "tool": "json"}
  | |  +{"pattern": "glob:dir-2/file 3.json", "tool": "json"}
  | |  diff -r 7a251aee7fec -r 7e4070817d0b dir-2/file 3.json
  | |  --- a/dir-2/file 3.json	Thu Jan 01 00:00:00 1970 +0000
  | |  +++ b/dir-2/file 3.json	Thu Jan 01 00:00:00 1970 +0000
  | |  @@ -1,1 +1,12 @@
  | |  -{"key1": "hello", "key2": [3, 1, 8, -1, 19, 2], "key3": "babar"}
  | |  +{
  | |  +    "key1": "hello",
  | |  +    "key2": [
  | |  +        3,
  | |  +        1,
  | |  +        8,
  | |  +        -1,
  | |  +        19,
  | |  +        2
  | |  +    ],
  | |  +    "key3": "babar"
  | |  +}
  | |  diff -r 7a251aee7fec -r 7e4070817d0b dir-2/file-1.json
  | |  --- a/dir-2/file-1.json	Thu Jan 01 00:00:00 1970 +0000
  | |  +++ b/dir-2/file-1.json	Thu Jan 01 00:00:00 1970 +0000
  | |  @@ -1,1 +1,17 @@
  | |  -{"key1": [44,50,82], "key2": [4, 8, -4, 5], "key3": ["Asia", "Europe"]}
  | |  +{
  | |  +    "key1": [
  | |  +        44,
  | |  +        50,
  | |  +        82
  | |  +    ],
  | |  +    "key2": [
  | |  +        4,
  | |  +        8,
  | |  +        -4,
  | |  +        5
  | |  +    ],
  | |  +    "key3": [
  | |  +        "Asia",
  | |  +        "Europe"
  | |  +    ]
  | |  +}
  | |
  | o  changeset:   2:7a251aee7fec
  |/   user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    summary:     format dir1 as a whole
  |
  |    diff -r 37aedc05b31a -r 7a251aee7fec .hg-format-source
  |    --- a/.hg-format-source	Thu Jan 01 00:00:00 1970 +0000
  |    +++ b/.hg-format-source	Thu Jan 01 00:00:00 1970 +0000
  |    @@ -1,1 +1,2 @@
  |     {"pattern": "glob:root-file.json", "tool": "json"}
  |    +{"pattern": "glob:dir-1/**", "tool": "json"}
  |    diff -r 37aedc05b31a -r 7a251aee7fec dir-1/file-1.json
  |    --- a/dir-1/file-1.json	Thu Jan 01 00:00:00 1970 +0000
  |    +++ b/dir-1/file-1.json	Thu Jan 01 00:00:00 1970 +0000
  |    @@ -1,1 +1,18 @@
  |    -{"key1": [42,53,78], "key2": [9,3,8,1], "key3": ["London", "Paris", "Tokyo"]}
  |    +{
  |    +    "key1": [
  |    +        42,
  |    +        53,
  |    +        78
  |    +    ],
  |    +    "key2": [
  |    +        9,
  |    +        3,
  |    +        8,
  |    +        1
  |    +    ],
  |    +    "key3": [
  |    +        "London",
  |    +        "Paris",
  |    +        "Tokyo"
  |    +    ]
  |    +}
  |    diff -r 37aedc05b31a -r 7a251aee7fec dir-1/file-2.json
  |    --- a/dir-1/file-2.json	Thu Jan 01 00:00:00 1970 +0000
  |    +++ b/dir-1/file-2.json	Thu Jan 01 00:00:00 1970 +0000
  |    @@ -1,1 +1,18 @@
  |    -{"key1": 1, "key2": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], "key3": [54]}
  |    +{
  |    +    "key1": 1,
  |    +    "key2": [
  |    +        0,
  |    +        1,
  |    +        2,
  |    +        3,
  |    +        4,
  |    +        5,
  |    +        6,
  |    +        7,
  |    +        8,
  |    +        9
  |    +    ],
  |    +    "key3": [
  |    +        54
  |    +    ]
  |    +}
  |
  o  changeset:   1:37aedc05b31a
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     format the root-file
  |
  |  diff -r bdc6e1fea625 -r 37aedc05b31a .hg-format-source
  |  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  |  +++ b/.hg-format-source	Thu Jan 01 00:00:00 1970 +0000
  |  @@ -0,0 +1,1 @@
  |  +{"pattern": "glob:root-file.json", "tool": "json"}
  |  diff -r bdc6e1fea625 -r 37aedc05b31a root-file.json
  |  --- a/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  |  +++ b/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  |  @@ -1,1 +1,14 @@
  |  -{"key1": 1, "key2": [5,6,7,8], "key3": ["arthur", "babar", "celeste"]}
  |  +{
  |  +    "key1": 1,
  |  +    "key2": [
  |  +        5,
  |  +        6,
  |  +        7,
  |  +        8
  |  +    ],
  |  +    "key3": [
  |  +        "arthur",
  |  +        "babar",
  |  +        "celeste"
  |  +    ]
  |  +}
  |
  o  changeset:   0:bdc6e1fea625
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     initial commit
  
     diff -r 000000000000 -r bdc6e1fea625 dir-1/file-1.json
     --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
     +++ b/dir-1/file-1.json	Thu Jan 01 00:00:00 1970 +0000
     @@ -0,0 +1,1 @@
     +{"key1": [42,53,78], "key2": [9,3,8,1], "key3": ["London", "Paris", "Tokyo"]}
     diff -r 000000000000 -r bdc6e1fea625 dir-1/file-2.json
     --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
     +++ b/dir-1/file-2.json	Thu Jan 01 00:00:00 1970 +0000
     @@ -0,0 +1,1 @@
     +{"key1": 1, "key2": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], "key3": [54]}
     diff -r 000000000000 -r bdc6e1fea625 dir-2/file 3.json
     --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
     +++ b/dir-2/file 3.json	Thu Jan 01 00:00:00 1970 +0000
     @@ -0,0 +1,1 @@
     +{"key1": "hello", "key2": [3, 1, 8, -1, 19, 2], "key3": "babar"}
     diff -r 000000000000 -r bdc6e1fea625 dir-2/file-1.json
     --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
     +++ b/dir-2/file-1.json	Thu Jan 01 00:00:00 1970 +0000
     @@ -0,0 +1,1 @@
     +{"key1": [44,50,82], "key2": [4, 8, -4, 5], "key3": ["Asia", "Europe"]}
     diff -r 000000000000 -r bdc6e1fea625 dir-2/file-2.json
     --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
     +++ b/dir-2/file-2.json	Thu Jan 01 00:00:00 1970 +0000
     @@ -0,0 +1,3 @@
     +{"key1": 6,
     +"key2": [3, 5, -2, 3, 4, 11, 10, -4, 8, 9],
     +"key3": [898, 32543, 2342]}
     diff -r 000000000000 -r bdc6e1fea625 root-file.json
     --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
     +++ b/root-file.json	Thu Jan 01 00:00:00 1970 +0000
     @@ -0,0 +1,1 @@
     +{"key1": 1, "key2": [5,6,7,8], "key3": ["arthur", "babar", "celeste"]}
  

Actual merge

  $ hg diff -r 1 -r B_B .hg-format-source
  $ hg diff -r 1 -r default .hg-format-source
  diff -r 37aedc05b31a -r d5f5eb5c9a36 .hg-format-source
  --- a/.hg-format-source	Thu Jan 01 00:00:00 1970 +0000
  +++ b/.hg-format-source	Thu Jan 01 00:00:00 1970 +0000* (glob)
  @@ -1,1 +1,4 @@
   {"pattern": "glob:root-file.json", "tool": "json"}
  +{"pattern": "glob:dir-1/**", "tool": "json"}
  +{"pattern": "glob:dir-2/file-1.json", "tool": "json"}
  +{"pattern": "glob:dir-2/file 3.json", "tool": "json"}
  $ hg status
  $ hg up -C B_B
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg merge default
  merging dir-1/file-2.json
  merging dir-2/file 3.json
  merging root-file.json
  3 files updated, 3 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)
  $ hg log -GT compact
  @  10[tip]   7414847d3de4   1970-01-01 00:00 +0000   test
  |    update d2f2 and d2f3
  |
  o  9:5   039f5de9b75e   1970-01-01 00:00 +0000   test
  |    update root-file and d1f2
  |
  | @  8   d5f5eb5c9a36   1970-01-01 00:00 +0000   test
  | |    update d1f2 and d2f1
  | |
  | o  7   fd4a3a3a3955   1970-01-01 00:00 +0000   test
  | |    update d1f1
  | |
  | o  6:3   db9ac9e49e2d   1970-01-01 00:00 +0000   test
  | |    update root-file
  | |
  o |  5   ca3f6acf64a5   1970-01-01 00:00 +0000   test
  | |    conflicting update
  | |
  o |  4:1   ade957fdb911   1970-01-01 00:00 +0000   test
  | |    update key 1
  | |
  | o  3   7e4070817d0b   1970-01-01 00:00 +0000   test
  | |    format some dir2 with explicite pattern
  | |
  | o  2   7a251aee7fec   1970-01-01 00:00 +0000   test
  |/     format dir1 as a whole
  |
  o  1   37aedc05b31a   1970-01-01 00:00 +0000   test
  |    format the root-file
  |
  o  0   bdc6e1fea625   1970-01-01 00:00 +0000   test
       initial commit
  
  $ hg diff -r 'p1()'
  diff -r 7414847d3de4 .hg-format-source
  --- a/.hg-format-source	Thu Jan 01 00:00:00 1970 +0000
  +++ b/.hg-format-source	* (glob)
  @@ -1,1 +1,4 @@
   {"pattern": "glob:root-file.json", "tool": "json"}
  +{"pattern": "glob:dir-1/**", "tool": "json"}
  +{"pattern": "glob:dir-2/file-1.json", "tool": "json"}
  +{"pattern": "glob:dir-2/file 3.json", "tool": "json"}
  diff -r 7414847d3de4 dir-1/file-1.json
  --- a/dir-1/file-1.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/dir-1/file-1.json	* (glob)
  @@ -1,1 +1,18 @@
  -{"key1": [42,53,78], "key2": [9,3,8,1], "key3": ["London", "Paris", "Tokyo"]}
  +{
  +    "key1": [
  +        42,
  +        53,
  +        76
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
  diff -r 7414847d3de4 dir-1/file-2.json
  --- a/dir-1/file-2.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/dir-1/file-2.json	* (glob)
  @@ -1,1 +1,18 @@
  -{"key1": 4, "key2": [0, 1, 3, 3, 7, 5, 9, 7, 8, 9], "key3": [54]}
  +{
  +    "key1": 4,
  +    "key2": [
  +        0,
  +        1,
  +        3,
  +        3,
  +        7,
  +        5,
  +        9,
  +        7,
  +        8,
  +        9
  +    ],
  +    "key3": [
  +        54
  +    ]
  +}
  diff -r 7414847d3de4 dir-2/file 3.json
  --- a/dir-2/file 3.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/dir-2/file 3.json	* (glob)
  @@ -1,1 +1,12 @@
  -{"key1": "hello", "key2": [6, 1, 8, -1, 19, 2], "key3": "Babar"}
  +{
  +    "key1": "hello",
  +    "key2": [
  +        6,
  +        1,
  +        8,
  +        -1,
  +        19,
  +        2
  +    ],
  +    "key3": "Babar"
  +}
  diff -r 7414847d3de4 dir-2/file-1.json
  --- a/dir-2/file-1.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/dir-2/file-1.json	* (glob)
  @@ -1,1 +1,18 @@
  -{"key1": [44,50,82], "key2": [4, 8, -4, 5], "key3": ["Asia", "Europe"]}
  +{
  +    "key1": [
  +        44,
  +        50,
  +        86
  +    ],
  +    "key2": [
  +        4,
  +        8,
  +        -4,
  +        5
  +    ],
  +    "key3": [
  +        "Asia",
  +        "Europe",
  +        "Oceania"
  +    ]
  +}
  diff -r 7414847d3de4 root-file.json
  --- a/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/root-file.json	* (glob)
  @@ -9,6 +9,7 @@
       "key3": [
           "arthur",
           "babar",
  -        "celeste"
  +        "celeste",
  +        "pomme"
       ]
   }
  $ hg diff -r 'p2()'
  diff -r d5f5eb5c9a36 dir-1/file-2.json
  --- a/dir-1/file-2.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/dir-1/file-2.json	* (glob)
  @@ -3,11 +3,11 @@
       "key2": [
           0,
           1,
  -        2,
  +        3,
           3,
  -        4,
  +        7,
           5,
  -        6,
  +        9,
           7,
           8,
           9
  diff -r d5f5eb5c9a36 dir-2/file 3.json
  --- a/dir-2/file 3.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/dir-2/file 3.json	* (glob)
  @@ -1,12 +1,12 @@
   {
       "key1": "hello",
       "key2": [
  -        3,
  +        6,
           1,
           8,
           -1,
           19,
           2
       ],
  -    "key3": "babar"
  +    "key3": "Babar"
   }
  diff -r d5f5eb5c9a36 dir-2/file-2.json
  --- a/dir-2/file-2.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/dir-2/file-2.json	* (glob)
  @@ -1,3 +1,3 @@
   {"key1": 6,
   "key2": [3, 5, -2, 3, 4, 11, 10, -4, 8, 9],
  -"key3": [898, 32543, 2342]}
  +"key3": [898, 32543, 2336]}
  diff -r d5f5eb5c9a36 root-file.json
  --- a/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/root-file.json	* (glob)
  @@ -1,5 +1,5 @@
   {
  -    "key1": 1,
  +    "key1": 1337,
       "key2": [
           5,
           6,

Merge from a sub directory
==========================

  $ hg up -C .
  6 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ cd dir-1
  $ hg merge default
  merging dir-1/file-2.json
  merging dir-2/file 3.json
  merging root-file.json
  3 files updated, 3 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)
  $ hg commit -qm 'Merge commit'
  $ cd ..

Preserve flags
==============

  $ mkdir flags
  $ cat << EOF > flags/executable.json
  > {}
  > EOF
  $ chmod +x flags/executable.json
  $ hg add -q flags/*
  $ hg ci -qm "Add flags subdir"
  $ hg format-source json glob:flags/* -m 'Executable file formatted'
  $ ls -l flags/* | cut -b 1-10
  -rwxr-xr-x

Test error case
===============

Current limitation
------------------

not at repository root

  $ cd dir-1
  $ hg format-source json glob:file-2.json
  abort: format-source must be run from repository root
  (cd $TESTTMP/test_repo)
  [255]
  $ cd ..

legitimate error
----------------

no pattern

  $ hg format-source json
  abort: no files specified
  [255]

unknown tool

  $ hg format-source babar-tool glob:file-2.json
  abort: unknow format tool: babar-tool (no 'format-source.babar-tool' config)
  [255]

space in tool

  $ hg format-source 'babar tooling' 'glob:**'
  abort: tool name cannot contains space: 'babar tooling'
  [255]

Uncommited changes

  $ echo a >> root-file.json
  $ hg format-source json 'glob:root-file.json'
  abort: uncommitted changes
  [255]

Merge with an undefined tool

  $ hg up -qC 0
  $ cat << EOF > root-file.json
  > {"key1": 1, "key2": [5,6,7,8], "key3": ["Arthur", "babar", "celeste"]}
  > EOF
  $ hg diff
  diff -r bdc6e1fea625 root-file.json
  --- a/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/root-file.json	* (glob)
  @@ -1,1 +1,1 @@
  -{"key1": 1, "key2": [5,6,7,8], "key3": ["arthur", "babar", "celeste"]}
  +{"key1": 1, "key2": [5,6,7,8], "key3": ["Arthur", "babar", "celeste"]}
  $ hg up --merge default --config 'format-source.json='
  format-source, no command defined for 'json', skipping formating: 'root-file.json'
  format-source, no command defined for 'json', skipping formating: 'root-file.json'
  merging root-file.json
  format-source, no command defined for 'json', skipping formating: 'root-file.json'
  format-source, no command defined for 'json', skipping formating: 'root-file.json'
  warning: conflicts while merging root-file.json! (edit, then use 'hg resolve --mark')
  5 files updated, 0 files merged, 0 files removed, 1 files unresolved
  use 'hg resolve' to retry unresolved file merges
  [1]

Test formatting tool with an invalid mode

  $ hg up -C .
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved

  $ hg format-source 'json_invalid_input' 'glob:**.json'
  abort: Tool json_invalid_input has an invalid input mode: invalid
  [255]

  $ hg format-source 'json_invalid_output' 'glob:**.json'
  abort: Tool json_invalid_output has an invalid output mode: invalid
  [255]

Test formatting tool which is crashing

  $ hg format-source 'json_failing' 'glob:**.json'
  abort: json_failing: python exited with status 1 (hg46 !)
  abort: json_failing: python ('exited with status 1', 1) (no-hg46 !)
  [255]

  $ hg format-source 'json_failing' 'glob:**.json' --debug
  running python $TESTTMP/json_failing.py
  format-source: [json_failing] Traceback (most recent call last):
  format-source: [json_failing]   File "$TESTTMP/json_failing.py", line 3, in <module>
  format-source: [json_failing]     with open(sys.argv[1], 'rb') as infile:
  format-source: [json_failing] IndexError: list index out of range
  abort: json_failing: python exited with status 1 (hg46 !)
  abort: json_failing: python ('exited with status 1', 1) (no-hg46 !)
  [255]
