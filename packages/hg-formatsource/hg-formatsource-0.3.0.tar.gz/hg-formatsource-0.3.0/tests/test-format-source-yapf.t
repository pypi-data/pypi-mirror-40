#require yapf

Basic init

  $ code_root=`dirname $TESTDIR`

  $ cat << EOF >> $HGRCPATH
  > [extensions]
  > formatsource=${code_root}/hgext3rd/formatsource.py
  > [default]
  > format-source=--date '0 0'
  > [ui]
  > merge=:merge3
  > EOF
  $ HGMERGE=:merge3

  $ hg init default-io-modes

  $ cd default-io-modes

  $ touch ROOT

  $ hg commit -Aq -m "Root"

Add python file
===============

  $ hg up -Cq 0

  $ cat << EOF >> yapf-test-file.py
  > 
  > l = [1,
  >      2,
  >      3,
  > ]
  > EOF

  $ hg add yapf-test-file.py

  $ hg commit -q -m "Add yapf test file"

  $ hg format-source --date '0 0' yapf glob:yapf-test-file.py -m 'format using yapf'

  $ hg export .
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID 1542eedad6a54b3038f6d14b77ce87fe2d9e6446
  # Parent  2f19add4f218eae057ea8765da81baeb86140ca9
  format using yapf
  
  diff -r 2f19add4f218 -r 1542eedad6a5 .hg-format-source
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/.hg-format-source	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +{"configpaths": [".style.yapf", "setup.cfg"], "pattern": "glob:yapf-test-file.py", "tool": "yapf"}
  diff -r 2f19add4f218 -r 1542eedad6a5 yapf-test-file.py
  --- a/yapf-test-file.py	Thu Jan 01 00:00:00 1970 +0000
  +++ b/yapf-test-file.py	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,5 +1,5 @@
  -
  -l = [1,
  -     2,
  -     3,
  +l = [
  +    1,
  +    2,
  +    3,
   ]

Make some changes
=================

  $ cat << EOF > yapf-test-file.py
  > l = [1, 2, 3, 4,5,6,7,8,9,10]
  > EOF

  $ hg commit -q -m "Update yapf test file"

  $ hg export .
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID f2c87b95dde077991ad2b4be5e46680e9193b51c
  # Parent  1542eedad6a54b3038f6d14b77ce87fe2d9e6446
  Update yapf test file
  
  diff -r 1542eedad6a5 -r f2c87b95dde0 yapf-test-file.py
  --- a/yapf-test-file.py	Thu Jan 01 00:00:00 1970 +0000
  +++ b/yapf-test-file.py	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,5 +1,1 @@
  -l = [
  -    1,
  -    2,
  -    3,
  -]
  +l = [1, 2, 3, 4,5,6,7,8,9,10]

Add another change on another branch
====================================

  $ hg up -Cq 2

  $ cat << EOF > yapf-test-file.py
  > l = [
  >     1,
  >     2,
  >     3,
  > ]
  > 
  > d = {"key": "value"}
  > EOF

  $ hg commit -m "Add dict"
  created new head

  $ hg export .
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID 731dbbf53925dfc2d3022769b0055f794de1a1f4
  # Parent  1542eedad6a54b3038f6d14b77ce87fe2d9e6446
  Add dict
  
  diff -r 1542eedad6a5 -r 731dbbf53925 yapf-test-file.py
  --- a/yapf-test-file.py	Thu Jan 01 00:00:00 1970 +0000
  +++ b/yapf-test-file.py	Thu Jan 01 00:00:00 1970 +0000
  @@ -3,3 +3,5 @@
       2,
       3,
   ]
  +
  +d = {"key": "value"}

Add a config file
=================

  $ cat << EOF >> .style.yapf
  > [style]
  > based_on_style = pep8
  > column_limit = 10
  > EOF

  $ hg add .style.yapf

  $ yapf yapf-test-file.py
  l = [
      1,
      2,
      3,
  ]
  
  d = {
      "key":
      "value"
  }

  $ hg commit -m "Add yapf config file"

  $ hg export .
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID f07a5f5162e037dee0d082151c3e74e0f9f297cf
  # Parent  731dbbf53925dfc2d3022769b0055f794de1a1f4
  Add yapf config file
  
  diff -r 731dbbf53925 -r f07a5f5162e0 .style.yapf
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/.style.yapf	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,3 @@
  +[style]
  +based_on_style = pep8
  +column_limit = 10


Test merge
==========

  $ hg log -G -T compact
  @  5[tip]   f07a5f5162e0   1970-01-01 00:00 +0000   test
  |    Add yapf config file
  |
  o  4:2   731dbbf53925   1970-01-01 00:00 +0000   test
  |    Add dict
  |
  | o  3   f2c87b95dde0   1970-01-01 00:00 +0000   test
  |/     Update yapf test file
  |
  o  2   1542eedad6a5   1970-01-01 00:00 +0000   test
  |    format using yapf
  |
  o  1   2f19add4f218   1970-01-01 00:00 +0000   test
  |    Add yapf test file
  |
  o  0   b00443a54871   1970-01-01 00:00 +0000   test
       Root
  

  $ hg merge
  setup.cfg: No such file or directory
  merging yapf-test-file.py
  0 files updated, 1 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)

  $ hg diff
  diff -r f07a5f5162e0 yapf-test-file.py
  --- a/yapf-test-file.py	Thu Jan 01 00:00:00 1970 +0000
  +++ b/yapf-test-file.py	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,7 +1,9 @@
   l = [
  -    1,
  -    2,
  -    3,
  +    1, 2,
  +    3, 4,
  +    5, 6,
  +    7, 8,
  +    9, 10
   ]
   
   d = {"key": "value"}

  $ hg commit -m "Merge"

  $ hg export .
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID d869e92be3c18e1b389e74ec848cc5915a5b9cfc
  # Parent  f07a5f5162e037dee0d082151c3e74e0f9f297cf
  # Parent  f2c87b95dde077991ad2b4be5e46680e9193b51c
  Merge
  
  diff -r f07a5f5162e0 -r d869e92be3c1 yapf-test-file.py
  --- a/yapf-test-file.py	Thu Jan 01 00:00:00 1970 +0000
  +++ b/yapf-test-file.py	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,7 +1,9 @@
   l = [
  -    1,
  -    2,
  -    3,
  +    1, 2,
  +    3, 4,
  +    5, 6,
  +    7, 8,
  +    9, 10
   ]
   
   d = {"key": "value"}

  $ hg export . --switch-parent
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID d869e92be3c18e1b389e74ec848cc5915a5b9cfc
  # Parent  f2c87b95dde077991ad2b4be5e46680e9193b51c
  # Parent  f07a5f5162e037dee0d082151c3e74e0f9f297cf
  Merge
  
  diff -r f2c87b95dde0 -r d869e92be3c1 .style.yapf
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/.style.yapf	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,3 @@
  +[style]
  +based_on_style = pep8
  +column_limit = 10
  diff -r f2c87b95dde0 -r d869e92be3c1 yapf-test-file.py
  --- a/yapf-test-file.py	Thu Jan 01 00:00:00 1970 +0000
  +++ b/yapf-test-file.py	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,1 +1,9 @@
  -l = [1, 2, 3, 4,5,6,7,8,9,10]
  +l = [
  +    1, 2,
  +    3, 4,
  +    5, 6,
  +    7, 8,
  +    9, 10
  +]
  +
  +d = {"key": "value"}
