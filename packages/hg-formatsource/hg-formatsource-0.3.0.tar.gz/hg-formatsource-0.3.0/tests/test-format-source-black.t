#require black

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

  $ cat << EOF >> black-test-file.py
  > 
  > l = [1,
  >      2,
  >      3,
  > ]
  > EOF

  $ hg add black-test-file.py

  $ hg commit -q -m "Add black test file"

Black is tacky
==============

  $ export LC_ALL=C.UTF-8
  $ export LANG=C.UTF-8

  $ hg format-source --date '0 0' black glob:black-test-file.py -m 'format using black'

  $ hg export .
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID fe243a8c7225b20a7c4ba989bcaf0b902706003b
  # Parent  c2cba438e30a5308a74134db58441e4e7108a5fb
  format using black
  
  diff -r c2cba438e30a -r fe243a8c7225 .hg-format-source
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/.hg-format-source	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +{"configpaths": ["pyproject.toml"], "pattern": "glob:black-test-file.py", "tool": "black"}
  diff -r c2cba438e30a -r fe243a8c7225 black-test-file.py
  --- a/black-test-file.py	Thu Jan 01 00:00:00 1970 +0000
  +++ b/black-test-file.py	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,5 +1,1 @@
  -
  -l = [1,
  -     2,
  -     3,
  -]
  +l = [1, 2, 3]

Make some changes
=================

  $ cat << EOF > black-test-file.py
  > l = [1, 2, 3, 4,5,6,7,8,9,10]
  > EOF

  $ hg commit -q -m "Update black test file"

  $ hg export .
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID 14c2f64a0fdfb6a73a13fd2ddf0c06960c076668
  # Parent  fe243a8c7225b20a7c4ba989bcaf0b902706003b
  Update black test file
  
  diff -r fe243a8c7225 -r 14c2f64a0fdf black-test-file.py
  --- a/black-test-file.py	Thu Jan 01 00:00:00 1970 +0000
  +++ b/black-test-file.py	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,1 +1,1 @@
  -l = [1, 2, 3]
  +l = [1, 2, 3, 4,5,6,7,8,9,10]

Add another change on another branch
====================================

  $ hg up -Cq 2

  $ cat << EOF > black-test-file.py
  > l = [1, 2, 3]
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
  # Node ID c00f52957408a7a63e197f6adc05ba6923119282
  # Parent  fe243a8c7225b20a7c4ba989bcaf0b902706003b
  Add dict
  
  diff -r fe243a8c7225 -r c00f52957408 black-test-file.py
  --- a/black-test-file.py	Thu Jan 01 00:00:00 1970 +0000
  +++ b/black-test-file.py	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,1 +1,3 @@
   l = [1, 2, 3]
  +
  +d = {"key": "value"}


Add a config file
=================

  $ cat << EOF >> pyproject.toml
  > [tool.black]
  > line-length = 10
  > EOF

  $ hg add pyproject.toml

  $ black black-test-file.py
  reformatted black-test-file.py
  All done! \xe2\x9c\xa8 \xf0\x9f\x8d\xb0 \xe2\x9c\xa8 (esc)
  1 file reformatted.

  $ hg commit -m "Add black config file"

  $ hg export .
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID b31e188862c320dac43369e6dc70dda740fd0de7
  # Parent  c00f52957408a7a63e197f6adc05ba6923119282
  Add black config file
  
  diff -r c00f52957408 -r b31e188862c3 black-test-file.py
  --- a/black-test-file.py	Thu Jan 01 00:00:00 1970 +0000
  +++ b/black-test-file.py	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,3 +1,9 @@
  -l = [1, 2, 3]
  +l = [
  +    1,
  +    2,
  +    3,
  +]
   
  -d = {"key": "value"}
  +d = {
  +    "key": "value"
  +}
  diff -r c00f52957408 -r b31e188862c3 pyproject.toml
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/pyproject.toml	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,2 @@
  +[tool.black]
  +line-length = 10


Test merge
==========

  $ hg log -G -T compact
  @  5[tip]   b31e188862c3   1970-01-01 00:00 +0000   test
  |    Add black config file
  |
  o  4:2   c00f52957408   1970-01-01 00:00 +0000   test
  |    Add dict
  |
  | o  3   14c2f64a0fdf   1970-01-01 00:00 +0000   test
  |/     Update black test file
  |
  o  2   fe243a8c7225   1970-01-01 00:00 +0000   test
  |    format using black
  |
  o  1   c2cba438e30a   1970-01-01 00:00 +0000   test
  |    Add black test file
  |
  o  0   b00443a54871   1970-01-01 00:00 +0000   test
       Root
  

  $ hg merge
  merging black-test-file.py
  0 files updated, 1 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)

  $ hg commit -m "Merge"

  $ hg export .
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID 46bf4e84548d826d5cad2bfc3171eeeac419d163
  # Parent  b31e188862c320dac43369e6dc70dda740fd0de7
  # Parent  14c2f64a0fdfb6a73a13fd2ddf0c06960c076668
  Merge
  
  diff -r b31e188862c3 -r 46bf4e84548d black-test-file.py
  --- a/black-test-file.py	Thu Jan 01 00:00:00 1970 +0000
  +++ b/black-test-file.py	Thu Jan 01 00:00:00 1970 +0000
  @@ -2,6 +2,13 @@
       1,
       2,
       3,
  +    4,
  +    5,
  +    6,
  +    7,
  +    8,
  +    9,
  +    10,
   ]
   
   d = {

  $ hg export . --switch-parent
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID 46bf4e84548d826d5cad2bfc3171eeeac419d163
  # Parent  14c2f64a0fdfb6a73a13fd2ddf0c06960c076668
  # Parent  b31e188862c320dac43369e6dc70dda740fd0de7
  Merge
  
  diff -r 14c2f64a0fdf -r 46bf4e84548d black-test-file.py
  --- a/black-test-file.py	Thu Jan 01 00:00:00 1970 +0000
  +++ b/black-test-file.py	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,1 +1,16 @@
  -l = [1, 2, 3, 4,5,6,7,8,9,10]
  +l = [
  +    1,
  +    2,
  +    3,
  +    4,
  +    5,
  +    6,
  +    7,
  +    8,
  +    9,
  +    10,
  +]
  +
  +d = {
  +    "key": "value"
  +}
  diff -r 14c2f64a0fdf -r 46bf4e84548d pyproject.toml
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/pyproject.toml	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,2 @@
  +[tool.black]
  +line-length = 10
