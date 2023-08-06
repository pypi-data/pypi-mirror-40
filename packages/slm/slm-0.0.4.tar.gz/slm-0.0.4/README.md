slm - Seshat library manager
============================

slm (**s**eshat **l**ibrary **m**anager) is a tool for managing C/C++ library,
inspired by npm.

Usage
------
To initialize with slm, just type
```sh
$ slm init
```

This command will create `library.yml` file in current working directory.

library.yml
-----------

This file is a library spec file just like `package.json` file in
JavaScript package.

The file format is a valid YAML syntax.

An example of `library.yml` file.
```yaml
name: myawfullibrary
description: Description of the library.
version: 1.2.10
license: MIT
scripts:
  configure: ./configure.py
  make: make
```

Built-in variables
------------------

There are some variables send to your build tool when run build scripts.

### LIBRARY\_NAME
A string exactly `name` field in `library.yml` file.

### LIBRARY\_VERSION
A string exactly `version` field in `library.yml` file.

### SONAME
lib{LIBRARY\_NAME}.so.{MAJOR VERSION}

*MAJOR VERSION* is the first part of `LIBRARY_VERSION` which is separated with `.` character.

**e.g.** libmyawfullibrary.so.1

SemVer
------

All slm libraries should follow [Semantic Versioning 2.0](https://semver.org).

