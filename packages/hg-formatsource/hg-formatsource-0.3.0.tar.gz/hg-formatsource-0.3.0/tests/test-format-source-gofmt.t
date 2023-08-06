#require gofmt

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

Add go file
===========

  $ hg up -Cq 0

  $ cat << EOF >> gofmt-test-file.go
  > package main
  > 
  > 
  > import "fmt"
  > func main() {
  > fmt.Println("hello world")
  > }
  > EOF

  $ hg add gofmt-test-file.go

  $ hg commit -q -m "Add gofmt test file"

  $ hg format-source --date '0 0' gofmt glob:gofmt-test-file.go -m 'format using gofmt'

  $ hg export .
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID 6c3e4f939b78aff5b6cd521cd24e7aa78532c6d2
  # Parent  4a326a968063c41415733128bc30c29c84371b8f
  format using gofmt
  
  diff -r 4a326a968063 -r 6c3e4f939b78 .hg-format-source
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/.hg-format-source	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +{"pattern": "glob:gofmt-test-file.go", "tool": "gofmt"}
  diff -r 4a326a968063 -r 6c3e4f939b78 gofmt-test-file.go
  --- a/gofmt-test-file.go	Thu Jan 01 00:00:00 1970 +0000
  +++ b/gofmt-test-file.go	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,7 +1,7 @@
   package main
   
  -
   import "fmt"
  +
   func main() {
  -fmt.Println("hello world")
  +	fmt.Println("hello world")
   }

