Conan Example
=============

This repository contains a simple example of how to use conan to build an application comprising two libraries across OS's and architectures.

The application is bastardized from the [repository](https://github.com/memsharded/hello) used in the conan online tutorial.

The Example
=

The tutorial aims to show how we can take this simple arrangement of apps and libraries and Conan-ize so that we can ease building across architectures and platforms.

app
---

a client application that calls the function ```hello1()``` in lib1. 

lib1
----

a library consisting of single function, ```hello1()``` that calls the function ```hello()``` in lib2 

lib2
----

The bottom of the callstack. A library containing a single function ```hello()``.



