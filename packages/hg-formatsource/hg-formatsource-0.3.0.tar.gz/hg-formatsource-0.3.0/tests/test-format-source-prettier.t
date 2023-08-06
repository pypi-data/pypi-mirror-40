#require prettier

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

Add js file
===========

  $ hg up -Cq 0

  $ cat << EOF >> prettier-test-file.js
  > var express = require('express');
  > var app = express();
  > 
  > app.get('/', function (req, res) { res.send('Hello World!'); });
  > 
  > app.listen(3000, function () { console.log('Example app listening on port 3000!'); });
  > EOF

  $ hg add prettier-test-file.js

  $ hg commit -q -m "Add prettier test file"

  $ hg format-source --date '0 0' prettier glob:prettier-test-file.js -m 'format using prettier'

  $ hg export .
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID 144840d458adc1f5a523cc13b1c9921c6e118f5d
  # Parent  602ac470e240592c5253f97e9ddba74eb9d910b3
  format using prettier
  
  diff -r 602ac470e240 -r 144840d458ad .hg-format-source
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/.hg-format-source	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +{"configpaths": [".prettierrc", "prettier.yaml", ".prettier.yml", ".prettier.json", ".prettier.toml", "prettier.config.js", ".prettierrc.js", "package.json"], "pattern": "glob:prettier-test-file.js", "tool": "prettier"}
  diff -r 602ac470e240 -r 144840d458ad prettier-test-file.js
  --- a/prettier-test-file.js	Thu Jan 01 00:00:00 1970 +0000
  +++ b/prettier-test-file.js	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,6 +1,10 @@
  -var express = require('express');
  +var express = require("express");
   var app = express();
   
  -app.get('/', function (req, res) { res.send('Hello World!'); });
  +app.get("/", function(req, res) {
  +  res.send("Hello World!");
  +});
   
  -app.listen(3000, function () { console.log('Example app listening on port 3000!'); });
  +app.listen(3000, function() {
  +  console.log("Example app listening on port 3000!");
  +});

  $ cat prettier-test-file.js
  var express = require("express");
  var app = express();
  
  app.get("/", function(req, res) {
    res.send("Hello World!");
  });
  
  app.listen(3000, function() {
    console.log("Example app listening on port 3000!");
  });

Make some changes
=================

  $ cat << EOF > prettier-test-file.js
  > var express = require("express");
  > var app = express();
  > 
  > app.get("/", function(req, res) {
  >     res.send("Hello Foobar!");
  > });
  > 
  > app.listen(3000, function() {
  >   console.log("Example app listening on port 3000!");
  > });
  > EOF

  $ hg commit -q -m "Hello Foobar"

  $ hg export .
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID 9c2fb5d9c4f34ed233cec6c3cae173144d2bbacd
  # Parent  144840d458adc1f5a523cc13b1c9921c6e118f5d
  Hello Foobar
  
  diff -r 144840d458ad -r 9c2fb5d9c4f3 prettier-test-file.js
  --- a/prettier-test-file.js	Thu Jan 01 00:00:00 1970 +0000
  +++ b/prettier-test-file.js	Thu Jan 01 00:00:00 1970 +0000
  @@ -2,7 +2,7 @@
   var app = express();
   
   app.get("/", function(req, res) {
  -  res.send("Hello World!");
  +    res.send("Hello Foobar!");
   });
   
   app.listen(3000, function() {

Add another change on another branch
====================================

  $ hg up -Cq 2

  $ cat << EOF > prettier-test-file.js
  > var express = require("express");
  > var app = express();
  > 
  > app.get("/", function(req, res) {
  >     res.send("Hello World!");
  > });
  > app.get("/healthcheck", function(req, res) {
  >     res.send("OK!");
  > });
  > 
  > app.listen(3000, function() {
  >   console.log("Example app listening on port 3000!");
  > });
  > EOF

  $ hg commit -m "Add healthcheck"
  created new head

  $ hg export .
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID f67c2e67ba2d7321a29a49559f9ce31eb690b492
  # Parent  144840d458adc1f5a523cc13b1c9921c6e118f5d
  Add healthcheck
  
  diff -r 144840d458ad -r f67c2e67ba2d prettier-test-file.js
  --- a/prettier-test-file.js	Thu Jan 01 00:00:00 1970 +0000
  +++ b/prettier-test-file.js	Thu Jan 01 00:00:00 1970 +0000
  @@ -2,7 +2,10 @@
   var app = express();
   
   app.get("/", function(req, res) {
  -  res.send("Hello World!");
  +    res.send("Hello World!");
  +});
  +app.get("/healthcheck", function(req, res) {
  +    res.send("OK!");
   });
   
   app.listen(3000, function() {

Add a config file
=================

  $ cat << EOF > prettier.config.js
  > module.exports = {
  >   tabWidth: 2,
  >   singleQuote: true
  > };
  > EOF

  $ hg add prettier.config.js

  $ prettier --write prettier-test-file.js
  prettier-test-file.js *ms (glob)

  $ hg commit -m "Add prettier config file"

  $ hg export .
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID fcc3c2984c178384f51602ae92f9fbd73013cd69
  # Parent  f67c2e67ba2d7321a29a49559f9ce31eb690b492
  Add prettier config file
  
  diff -r f67c2e67ba2d -r fcc3c2984c17 prettier-test-file.js
  --- a/prettier-test-file.js	Thu Jan 01 00:00:00 1970 +0000
  +++ b/prettier-test-file.js	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,13 +1,13 @@
  -var express = require("express");
  +var express = require('express');
   var app = express();
   
  -app.get("/", function(req, res) {
  -    res.send("Hello World!");
  +app.get('/', function(req, res) {
  +  res.send('Hello World!');
   });
  -app.get("/healthcheck", function(req, res) {
  -    res.send("OK!");
  +app.get('/healthcheck', function(req, res) {
  +  res.send('OK!');
   });
   
   app.listen(3000, function() {
  -  console.log("Example app listening on port 3000!");
  +  console.log('Example app listening on port 3000!');
   });
  diff -r f67c2e67ba2d -r fcc3c2984c17 prettier.config.js
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/prettier.config.js	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,4 @@
  +module.exports = {
  +  tabWidth: 2,
  +  singleQuote: true
  +};


Test merge
==========

  $ hg log -G -T compact
  @  5[tip]   fcc3c2984c17   1970-01-01 00:00 +0000   test
  |    Add prettier config file
  |
  o  4:2   f67c2e67ba2d   1970-01-01 00:00 +0000   test
  |    Add healthcheck
  |
  | o  3   9c2fb5d9c4f3   1970-01-01 00:00 +0000   test
  |/     Hello Foobar
  |
  o  2   144840d458ad   1970-01-01 00:00 +0000   test
  |    format using prettier
  |
  o  1   602ac470e240   1970-01-01 00:00 +0000   test
  |    Add prettier test file
  |
  o  0   b00443a54871   1970-01-01 00:00 +0000   test
       Root
  

  $ hg merge
  .prettier.json: No such file or directory
  .prettier.toml: No such file or directory
  .prettier.yml: No such file or directory
  .prettierrc: No such file or directory
  .prettierrc.js: No such file or directory
  package.json: No such file or directory
  prettier.yaml: No such file or directory
  merging prettier-test-file.js
  0 files updated, 1 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)

  $ hg diff
  diff -r fcc3c2984c17 prettier-test-file.js
  --- a/prettier-test-file.js	Thu Jan 01 00:00:00 1970 +0000
  +++ b/prettier-test-file.js	Thu Jan 01 00:00:00 1970 +0000
  @@ -2,7 +2,7 @@
   var app = express();
   
   app.get('/', function(req, res) {
  -  res.send('Hello World!');
  +  res.send('Hello Foobar!');
   });
   app.get('/healthcheck', function(req, res) {
     res.send('OK!');

  $ hg commit -m "Merge"

  $ hg export .
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID 9ad110d2d07dd94195953f6b5c665062cd9a9750
  # Parent  fcc3c2984c178384f51602ae92f9fbd73013cd69
  # Parent  9c2fb5d9c4f34ed233cec6c3cae173144d2bbacd
  Merge
  
  diff -r fcc3c2984c17 -r 9ad110d2d07d prettier-test-file.js
  --- a/prettier-test-file.js	Thu Jan 01 00:00:00 1970 +0000
  +++ b/prettier-test-file.js	Thu Jan 01 00:00:00 1970 +0000
  @@ -2,7 +2,7 @@
   var app = express();
   
   app.get('/', function(req, res) {
  -  res.send('Hello World!');
  +  res.send('Hello Foobar!');
   });
   app.get('/healthcheck', function(req, res) {
     res.send('OK!');

  $ hg export . --switch-parent
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID 9ad110d2d07dd94195953f6b5c665062cd9a9750
  # Parent  9c2fb5d9c4f34ed233cec6c3cae173144d2bbacd
  # Parent  fcc3c2984c178384f51602ae92f9fbd73013cd69
  Merge
  
  diff -r 9c2fb5d9c4f3 -r 9ad110d2d07d prettier-test-file.js
  --- a/prettier-test-file.js	Thu Jan 01 00:00:00 1970 +0000
  +++ b/prettier-test-file.js	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,10 +1,13 @@
  -var express = require("express");
  +var express = require('express');
   var app = express();
   
  -app.get("/", function(req, res) {
  -    res.send("Hello Foobar!");
  +app.get('/', function(req, res) {
  +  res.send('Hello Foobar!');
  +});
  +app.get('/healthcheck', function(req, res) {
  +  res.send('OK!');
   });
   
   app.listen(3000, function() {
  -  console.log("Example app listening on port 3000!");
  +  console.log('Example app listening on port 3000!');
   });
  diff -r 9c2fb5d9c4f3 -r 9ad110d2d07d prettier.config.js
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/prettier.config.js	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,4 @@
  +module.exports = {
  +  tabWidth: 2,
  +  singleQuote: true
  +};
