#require clang-format

Test that the defaults configurations for known tools are working correctly

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

Testing clang-format tool
=========================

  $ hg up -Cq 0

  $ cat << EOF >> hello-world.cpp
  > #include <iostream>
  > 
  > int main() 
  > {
  >     std::cout << "Hello, World!";
  >     return 0;
  > }
  > EOF

  $ cat << EOF >> hello-world.c
  > #include<stdio.h>
  > 
  > int main(void) {
  >     printf("Hello World\n");
  >     return 0;
  > }
  > EOF

  $ hg add *
  ROOT already tracked!

  $ hg commit -q -m "Add clang-format test file"

  $ hg format-source --date '0 0' clang-format glob:hello-world.cpp -m 'format using clang-format'

  $ hg export .
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID 2734c7eabbf8b9036be264921b25ac478c61b680
  # Parent  a7685500a40492cd28a875655d9f40fb4ff1d8e1
  format using clang-format
  
  diff -r a7685500a404 -r 2734c7eabbf8 .hg-format-source
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/.hg-format-source	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +{"configpaths": [".clang-format", ".clang-format-ignore"], "pattern": "glob:hello-world.cpp", "tool": "clang-format"}
  diff -r a7685500a404 -r 2734c7eabbf8 hello-world.cpp
  --- a/hello-world.cpp	Thu Jan 01 00:00:00 1970 +0000
  +++ b/hello-world.cpp	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,7 +1,6 @@
   #include <iostream>
   
  -int main() 
  -{
  -    std::cout << "Hello, World!";
  -    return 0;
  +int main() {
  +  std::cout << "Hello, World!";
  +  return 0;
   }

  $ hg format-source --date '0 0' clang-format glob:hello-world.c -m 'format using clang-format'

  $ hg export .
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID d278ea5f0a787b6006352f966bd0aa70e6d5da86
  # Parent  2734c7eabbf8b9036be264921b25ac478c61b680
  format using clang-format
  
  diff -r 2734c7eabbf8 -r d278ea5f0a78 .hg-format-source
  --- a/.hg-format-source	Thu Jan 01 00:00:00 1970 +0000
  +++ b/.hg-format-source	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,1 +1,2 @@
   {"configpaths": [".clang-format", ".clang-format-ignore"], "pattern": "glob:hello-world.cpp", "tool": "clang-format"}
  +{"configpaths": [".clang-format", ".clang-format-ignore"], "pattern": "glob:hello-world.c", "tool": "clang-format"}
  diff -r 2734c7eabbf8 -r d278ea5f0a78 hello-world.c
  --- a/hello-world.c	Thu Jan 01 00:00:00 1970 +0000
  +++ b/hello-world.c	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,6 +1,6 @@
  -#include<stdio.h>
  +#include <stdio.h>
   
   int main(void) {
  -    printf("Hello World\n");
  -    return 0;
  +  printf("Hello World\n");
  +  return 0;
   }

Make some changes
=================

  $ cat << EOF > hello-world.cpp
  > #include <iostream>
  > 
  > int main() {
  >   std::cout << "Hello, FooBar!";
  >   return 0;
  > }
  > EOF

  $ cat << EOF > hello-world.c
  > #include <stdio.h>
  > 
  > int main(void) {
  >   printf("Hello FooBar\n");
  >   return 0;
  > }
  > EOF

  $ hg commit -q -m "Hello Foobar"

  $ hg export .
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID ee40ecf7ad518e082655a92073cb968d86c9883f
  # Parent  d278ea5f0a787b6006352f966bd0aa70e6d5da86
  Hello Foobar
  
  diff -r d278ea5f0a78 -r ee40ecf7ad51 hello-world.c
  --- a/hello-world.c	Thu Jan 01 00:00:00 1970 +0000
  +++ b/hello-world.c	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,6 +1,6 @@
   #include <stdio.h>
   
   int main(void) {
  -  printf("Hello World\n");
  +  printf("Hello FooBar\n");
     return 0;
   }
  diff -r d278ea5f0a78 -r ee40ecf7ad51 hello-world.cpp
  --- a/hello-world.cpp	Thu Jan 01 00:00:00 1970 +0000
  +++ b/hello-world.cpp	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,6 +1,6 @@
   #include <iostream>
   
   int main() {
  -  std::cout << "Hello, World!";
  +  std::cout << "Hello, FooBar!";
     return 0;
   }

Add another change on another branch
====================================

  $ hg up -Cq 3

  $ cat << EOF > hello-world.cpp
  > #include <iostream>
  > 
  > int main() {
  >   std::cout << "Hello, World!";
  >   return 0;
  > }
  > 
  > int answer() {
  >   return 42
  > }
  > EOF

  $ cat << EOF > hello-world.c
  > #include <stdio.h>
  > 
  > int main(void) {
  >   printf("Hello World\n");
  >   return 0;
  > }
  > 
  > int answer() {
  >   return 42
  > }
  > EOF

  $ hg commit -m "Exit 1"
  created new head

  $ hg export .
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID 4f34e4cc21d3e1a4b4cb73f7347660fcedbf868a
  # Parent  d278ea5f0a787b6006352f966bd0aa70e6d5da86
  Exit 1
  
  diff -r d278ea5f0a78 -r 4f34e4cc21d3 hello-world.c
  --- a/hello-world.c	Thu Jan 01 00:00:00 1970 +0000
  +++ b/hello-world.c	Thu Jan 01 00:00:00 1970 +0000
  @@ -4,3 +4,7 @@
     printf("Hello World\n");
     return 0;
   }
  +
  +int answer() {
  +  return 42
  +}
  diff -r d278ea5f0a78 -r 4f34e4cc21d3 hello-world.cpp
  --- a/hello-world.cpp	Thu Jan 01 00:00:00 1970 +0000
  +++ b/hello-world.cpp	Thu Jan 01 00:00:00 1970 +0000
  @@ -4,3 +4,7 @@
     std::cout << "Hello, World!";
     return 0;
   }
  +
  +int answer() {
  +  return 42
  +}

Add a config file
=================

  $ cat << EOF >> .clang-format
  > ---
  > IndentWidth:     4
  > ...
  > EOF

  $ hg add .clang-format

  $ clang-format -i hello-world.*

  $ hg commit -m "Add clang-format config file"

  $ hg export .
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID 6df595b0f6de2959ad594d5bb05b5da197f2c90b
  # Parent  4f34e4cc21d3e1a4b4cb73f7347660fcedbf868a
  Add clang-format config file
  
  diff -r 4f34e4cc21d3 -r 6df595b0f6de .clang-format
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/.clang-format	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,3 @@
  +---
  +IndentWidth:     4
  +...
  diff -r 4f34e4cc21d3 -r 6df595b0f6de hello-world.c
  --- a/hello-world.c	Thu Jan 01 00:00:00 1970 +0000
  +++ b/hello-world.c	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,10 +1,8 @@
   #include <stdio.h>
   
   int main(void) {
  -  printf("Hello World\n");
  -  return 0;
  +    printf("Hello World\n");
  +    return 0;
   }
   
  -int answer() {
  -  return 42
  -}
  +int answer() { return 42 }
  diff -r 4f34e4cc21d3 -r 6df595b0f6de hello-world.cpp
  --- a/hello-world.cpp	Thu Jan 01 00:00:00 1970 +0000
  +++ b/hello-world.cpp	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,10 +1,8 @@
   #include <iostream>
   
   int main() {
  -  std::cout << "Hello, World!";
  -  return 0;
  +    std::cout << "Hello, World!";
  +    return 0;
   }
   
  -int answer() {
  -  return 42
  -}
  +int answer() { return 42 }


Test merge
==========

  $ hg log -G -T compact
  @  6[tip]   6df595b0f6de   1970-01-01 00:00 +0000   test
  |    Add clang-format config file
  |
  o  5:3   4f34e4cc21d3   1970-01-01 00:00 +0000   test
  |    Exit 1
  |
  | o  4   ee40ecf7ad51   1970-01-01 00:00 +0000   test
  |/     Hello Foobar
  |
  o  3   d278ea5f0a78   1970-01-01 00:00 +0000   test
  |    format using clang-format
  |
  o  2   2734c7eabbf8   1970-01-01 00:00 +0000   test
  |    format using clang-format
  |
  o  1   a7685500a404   1970-01-01 00:00 +0000   test
  |    Add clang-format test file
  |
  o  0   b00443a54871   1970-01-01 00:00 +0000   test
       Root
  

  $ hg merge
  .clang-format-ignore: No such file or directory
  .clang-format-ignore: No such file or directory
  merging hello-world.c
  merging hello-world.cpp
  0 files updated, 2 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)

  $ hg commit -m "Merge"

  $ hg export .
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID 3a608854dc8e4679368aa879e3f8a1102f4ac06e
  # Parent  6df595b0f6de2959ad594d5bb05b5da197f2c90b
  # Parent  ee40ecf7ad518e082655a92073cb968d86c9883f
  Merge
  
  diff -r 6df595b0f6de -r 3a608854dc8e hello-world.c
  --- a/hello-world.c	Thu Jan 01 00:00:00 1970 +0000
  +++ b/hello-world.c	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,7 +1,7 @@
   #include <stdio.h>
   
   int main(void) {
  -    printf("Hello World\n");
  +    printf("Hello FooBar\n");
       return 0;
   }
   
  diff -r 6df595b0f6de -r 3a608854dc8e hello-world.cpp
  --- a/hello-world.cpp	Thu Jan 01 00:00:00 1970 +0000
  +++ b/hello-world.cpp	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,7 +1,7 @@
   #include <iostream>
   
   int main() {
  -    std::cout << "Hello, World!";
  +    std::cout << "Hello, FooBar!";
       return 0;
   }
   

  $ hg export . --switch-parent
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID 3a608854dc8e4679368aa879e3f8a1102f4ac06e
  # Parent  ee40ecf7ad518e082655a92073cb968d86c9883f
  # Parent  6df595b0f6de2959ad594d5bb05b5da197f2c90b
  Merge
  
  diff -r ee40ecf7ad51 -r 3a608854dc8e .clang-format
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/.clang-format	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,3 @@
  +---
  +IndentWidth:     4
  +...
  diff -r ee40ecf7ad51 -r 3a608854dc8e hello-world.c
  --- a/hello-world.c	Thu Jan 01 00:00:00 1970 +0000
  +++ b/hello-world.c	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,6 +1,8 @@
   #include <stdio.h>
   
   int main(void) {
  -  printf("Hello FooBar\n");
  -  return 0;
  +    printf("Hello FooBar\n");
  +    return 0;
   }
  +
  +int answer() { return 42 }
  diff -r ee40ecf7ad51 -r 3a608854dc8e hello-world.cpp
  --- a/hello-world.cpp	Thu Jan 01 00:00:00 1970 +0000
  +++ b/hello-world.cpp	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,6 +1,8 @@
   #include <iostream>
   
   int main() {
  -  std::cout << "Hello, FooBar!";
  -  return 0;
  +    std::cout << "Hello, FooBar!";
  +    return 0;
   }
  +
  +int answer() { return 42 }

Test that default configuration doesn't overwrite the user-defined one
######################################################################

  $ hg format-source --date '0 0' clang-format --config "format-source.clang-format=clang-format ---" glob:hello-world.cpp -m 'format using clang-format'
  abort: clang-format: clang-format exited with status 1
  [255]
