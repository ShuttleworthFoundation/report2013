Shuttleworth Foundation - Annual Report 2013
============================================

This repository contains the 2013 annual report infographic for the
Shuttleworth foundation. Jekyll input files are generated from the
`src/templates` and `src/data` files using the scripts provided and then
integrated into the main shuttleworthfoundation.org Jekyll page.

Checking out
------------

The repository is intended to be a submodule of the main
shuttleworthfoundation.org repository. The best way to get a copy of
this repository is to clone the main shuttleworthfoundation.org
repository with:

```shell
$ git clone --recursive git@github.com:ShuttleworthFoundation/shuttleworthfoundation.org.git
```
Requirements
--------

You will need python, python-virtualenv and jekyll installed on your machine.

Building
--------

The page is build using the included `Makefile`. Everything is
automated so it is very simple.

```shell  
$ make
```

The makefile is also automatically called from the main `Makefile`
added to the main shuttleworthfoundation.org repository, so building
the entire website should be as simple as calling `make` from the
root of the repository after doing a recursive clone.
