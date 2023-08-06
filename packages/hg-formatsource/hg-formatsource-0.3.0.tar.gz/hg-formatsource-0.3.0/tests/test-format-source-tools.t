#testcases in-file-out-pipe in-pipe-out-pipe inplace inplace-mode pipe-mode

Basic init

  $ code_root=`dirname $TESTDIR`

#if in-file-out-pipe

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

#endif

#if in-pipe-out-pipe

  $ cat >> json_format.py <<EOF
  > """ Auto-format the JSON code passed as stdin argument and output the
  > formatted code in stdout
  > """
  > import sys
  > import json
  > with sys.stdin:
  >     obj = json.load(sys.stdin)
  > with sys.stdout:
  >     json.dump(obj, sys.stdout, sort_keys=True, indent=4, separators=(',', ': '))
  >     sys.stdout.write("\n")
  > EOF

#endif

#if pipe-mode

  $ cat >> json_format.py <<EOF
  > """ Auto-format the JSON code passed as stdin argument and output the
  > formatted code in stdout
  > """
  > import sys
  > import json
  > with sys.stdin:
  >     obj = json.load(sys.stdin)
  > with sys.stdout:
  >     json.dump(obj, sys.stdout, sort_keys=True, indent=4, separators=(',', ': '))
  >     sys.stdout.write("\n")
  > EOF

#endif

#if inplace

  $ cat >> json_format.py <<EOF
  > """ Auto-format the JSON file passed as a command-line argument and write
  > the formatted code back to the file
  > """
  > import sys
  > import json
  > with open(sys.argv[1], 'rb') as infile:
  >     obj = json.load(infile)
  > with open(sys.argv[1], 'wb') as outfile:
  >     json.dump(obj, outfile, sort_keys=True, indent=4, separators=(',', ': '))
  >     outfile.write("\n")
  > EOF

#endif

#if inplace-mode

  $ cat >> json_format.py <<EOF
  > """ Auto-format the JSON file passed as a command-line argument and write
  > the formatted code back to the file
  > """
  > import sys
  > import json
  > with open(sys.argv[1], 'rb') as infile:
  >     obj = json.load(infile)
  > with open(sys.argv[1], 'wb') as outfile:
  >     json.dump(obj, outfile, sort_keys=True, indent=4, separators=(',', ': '))
  >     outfile.write("\n")
  > EOF

#endif

  $ cat << EOF >> $HGRCPATH
  > [extensions]
  > formatsource=${code_root}/hgext3rd/formatsource.py
  > rebase =
  > strip =
  > [default]
  > format-source=--date '0 0'
  > [ui]
  > merge=:merge3
  > [format-source]
  > json = python $TESTTMP/json_format.py
  > EOF
  $ HGMERGE=:merge3

#if in-file-out-pipe

  $ cat << EOF >> $HGRCPATH
  > json:mode.input = file
  > json:mode.output = pipe
  > EOF

#endif

#if in-pipe-out-pipe

  $ cat << EOF >> $HGRCPATH
  > json:mode.input = pipe
  > json:mode.output = pipe
  > EOF

#endif

#if pipe-mode

  $ cat << EOF >> $HGRCPATH
  > json:mode = pipe
  > EOF

#endif

#if inplace

  $ cat << EOF >> $HGRCPATH
  > json:mode.input = file
  > json:mode.output = file
  > EOF

#endif

#if inplace-mode

  $ cat << EOF >> $HGRCPATH
  > json:mode = file
  > EOF

#endif

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
