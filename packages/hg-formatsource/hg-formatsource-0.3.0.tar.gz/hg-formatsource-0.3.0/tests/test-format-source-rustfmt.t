#require rustfmt

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

Add rust file
=============

  $ hg up -Cq 0

  $ cat << EOF >> rustfmt-test-file.rust
  > fn main() {
  > println!("Hello World!");
  >  }
  > EOF

  $ hg add rustfmt-test-file.rust

  $ hg commit -q -m "Add rustfmt test file"

  $ hg format-source --date '0 0' rustfmt glob:rustfmt-test-file.rust -m 'format using rustfmt'

  $ hg export .
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID da06ed9e637567f3292f878115995000b0615c57
  # Parent  c48b5f3d107cd92cf61125f0edf67a844c2534ef
  format using rustfmt
  
  diff -r c48b5f3d107c -r da06ed9e6375 .hg-format-source
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/.hg-format-source	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +{"configpaths": ["rustfmt.toml", ".rustfmt.toml"], "pattern": "glob:rustfmt-test-file.rust", "tool": "rustfmt"}
  diff -r c48b5f3d107c -r da06ed9e6375 rustfmt-test-file.rust
  --- a/rustfmt-test-file.rust	Thu Jan 01 00:00:00 1970 +0000
  +++ b/rustfmt-test-file.rust	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,3 +1,3 @@
   fn main() {
  -println!("Hello World!");
  - }
  +    println!("Hello World!");
  +}

Make some changes
=================

  $ cat << EOF > rustfmt-test-file.rust
  > fn main() {
  >     println!("Hello Foobar!");
  > }
  > EOF

  $ hg commit -q -m "Hello Foobar"

  $ hg export .
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID ffe44beb4dbb8bdcda0af8ffa0566435ee99269e
  # Parent  da06ed9e637567f3292f878115995000b0615c57
  Hello Foobar
  
  diff -r da06ed9e6375 -r ffe44beb4dbb rustfmt-test-file.rust
  --- a/rustfmt-test-file.rust	Thu Jan 01 00:00:00 1970 +0000
  +++ b/rustfmt-test-file.rust	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,3 +1,3 @@
   fn main() {
  -    println!("Hello World!");
  +    println!("Hello Foobar!");
   }

Add another change on another branch
====================================

  $ hg up -Cq 2

  $ cat << EOF > rustfmt-test-file.rust
  > fn main() {
  >     println!("Hello World!");
  > }
  > 
  > pub fn answer(i:isize, j:isize, k:isize, l:isize, m:isize, n:isize, o:isize) -> isize {
  >     return i+j+k+l+m+n+o;
  > }
  > EOF

  $ hg commit -m "Add answer"
  created new head

  $ hg export .
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID 3ac66e772e5fec90f3f107741214845be02f8e99
  # Parent  da06ed9e637567f3292f878115995000b0615c57
  Add answer
  
  diff -r da06ed9e6375 -r 3ac66e772e5f rustfmt-test-file.rust
  --- a/rustfmt-test-file.rust	Thu Jan 01 00:00:00 1970 +0000
  +++ b/rustfmt-test-file.rust	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,3 +1,7 @@
   fn main() {
       println!("Hello World!");
   }
  +
  +pub fn answer(i:isize, j:isize, k:isize, l:isize, m:isize, n:isize, o:isize) -> isize {
  +    return i+j+k+l+m+n+o;
  +}

Add a config file
=================

  $ cat << EOF > .rustfmt.toml
  > hard_tabs = true
  > EOF

  $ hg add .rustfmt.toml

  $ rustfmt rustfmt-test-file.rust

  $ hg commit -m "Add rustfmt config file"

  $ hg export .
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID a9136bb8ecfc9431a6d8bea7d067e2132810f8f5
  # Parent  3ac66e772e5fec90f3f107741214845be02f8e99
  Add rustfmt config file
  
  diff -r 3ac66e772e5f -r a9136bb8ecfc .rustfmt.toml
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/.rustfmt.toml	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +hard_tabs = true
  diff -r 3ac66e772e5f -r a9136bb8ecfc rustfmt-test-file.rust
  --- a/rustfmt-test-file.rust	Thu Jan 01 00:00:00 1970 +0000
  +++ b/rustfmt-test-file.rust	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,7 +1,7 @@
   fn main() {
  -    println!("Hello World!");
  +	println!("Hello World!");
   }
   
  -pub fn answer(i:isize, j:isize, k:isize, l:isize, m:isize, n:isize, o:isize) -> isize {
  -    return i+j+k+l+m+n+o;
  +pub fn answer(i: isize, j: isize, k: isize, l: isize, m: isize, n: isize, o: isize) -> isize {
  +	return i + j + k + l + m + n + o;
   }


Test merge
==========

  $ hg log -G -T compact
  @  5[tip]   a9136bb8ecfc   1970-01-01 00:00 +0000   test
  |    Add rustfmt config file
  |
  o  4:2   3ac66e772e5f   1970-01-01 00:00 +0000   test
  |    Add answer
  |
  | o  3   ffe44beb4dbb   1970-01-01 00:00 +0000   test
  |/     Hello Foobar
  |
  o  2   da06ed9e6375   1970-01-01 00:00 +0000   test
  |    format using rustfmt
  |
  o  1   c48b5f3d107c   1970-01-01 00:00 +0000   test
  |    Add rustfmt test file
  |
  o  0   b00443a54871   1970-01-01 00:00 +0000   test
       Root
  

  $ hg merge
  rustfmt.toml: No such file or directory
  merging rustfmt-test-file.rust
  0 files updated, 1 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)

  $ hg diff
  diff -r a9136bb8ecfc rustfmt-test-file.rust
  --- a/rustfmt-test-file.rust	Thu Jan 01 00:00:00 1970 +0000
  +++ b/rustfmt-test-file.rust	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,5 +1,5 @@
   fn main() {
  -	println!("Hello World!");
  +	println!("Hello Foobar!");
   }
   
   pub fn answer(i: isize, j: isize, k: isize, l: isize, m: isize, n: isize, o: isize) -> isize {

  $ hg commit -m "Merge"

  $ hg export .
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID ade17b8eeb3872d45b4e47be50bf3846071a22a9
  # Parent  a9136bb8ecfc9431a6d8bea7d067e2132810f8f5
  # Parent  ffe44beb4dbb8bdcda0af8ffa0566435ee99269e
  Merge
  
  diff -r a9136bb8ecfc -r ade17b8eeb38 rustfmt-test-file.rust
  --- a/rustfmt-test-file.rust	Thu Jan 01 00:00:00 1970 +0000
  +++ b/rustfmt-test-file.rust	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,5 +1,5 @@
   fn main() {
  -	println!("Hello World!");
  +	println!("Hello Foobar!");
   }
   
   pub fn answer(i: isize, j: isize, k: isize, l: isize, m: isize, n: isize, o: isize) -> isize {

  $ hg export . --switch-parent
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID ade17b8eeb3872d45b4e47be50bf3846071a22a9
  # Parent  ffe44beb4dbb8bdcda0af8ffa0566435ee99269e
  # Parent  a9136bb8ecfc9431a6d8bea7d067e2132810f8f5
  Merge
  
  diff -r ffe44beb4dbb -r ade17b8eeb38 .rustfmt.toml
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/.rustfmt.toml	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +hard_tabs = true
  diff -r ffe44beb4dbb -r ade17b8eeb38 rustfmt-test-file.rust
  --- a/rustfmt-test-file.rust	Thu Jan 01 00:00:00 1970 +0000
  +++ b/rustfmt-test-file.rust	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,3 +1,7 @@
   fn main() {
  -    println!("Hello Foobar!");
  +	println!("Hello Foobar!");
   }
  +
  +pub fn answer(i: isize, j: isize, k: isize, l: isize, m: isize, n: isize, o: isize) -> isize {
  +	return i + j + k + l + m + n + o;
  +}
