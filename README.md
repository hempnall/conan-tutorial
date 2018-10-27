Conan Example
=============

This repository contains a simple example of how to use conan to build an application comprising two libraries across OS's and architectures.

The application is bastardized from the [repository](https://github.com/memsharded/hello) used in the conan online tutorial.


Thoughts
========

Conan seems to be biased towards CMake builds, although other build systems are supported.

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

The bottom of the callstack. A library containing a single function ```hello()```.

pkg
---

The packages will be defined and built in this folder. The package definition files need not be in the same source tree as the source code for the package.

Use case for a Package Management Tool
======================================

Installation
------------

Conan is a Python PIP package.

Assuming PIP is installed it is possible to install Conan as follows:

```
$ pip install --user conan
```

The Conan documentation provides warnings that Python 2 support in Conan will soon be deprecated. This tutorial still uses Python 2.

After installation, you can confirm Conan has been installed..

```
$ conan
Consumer commands
  install    Installs the requirements specified in a conanfile (.py or .txt).
  config     Manages configuration. Edits the conan.conf or installs config files.
  get        Gets a file or list a directory of a given reference or package.
  info       Gets information about the dependency graph of a recipe.
```

Offline Installation
--------------------

?????
To be useful to many organtisations, Conan must be able to operate in an offline environment. How do you do this?? ?????

Create Packages
---------------

Conan packages are specified by creating a ```Conanfile.py```.

This is a regular Python source file that performs the following tasks:
* defines metadata relating to your package
* gathers the source files for your library
* builds the source files in your package
* copies package distribution files into your package

Each of these steps can be customised by overriding methods in ConanFile class (defined within Conan)

> The source files (*.cpp, *.h) are not in the same directory as the package Conanfile.py. The source method will gather the sources from locations such as HTTP://, GIT or file copy.

A package can be created from the command line:

```
$ mkdir mypkg && cd mypkg
$ conan new Hello/0.1 -t
```
This creates a template ConanFile.py file for v0.1 of this package in the current directory. 

The ```-t``` flag tells conan to create a test_package subfolder. The test package is used to test that package can be consumed in a simple application.

The package is built using ```conan create```

```
$ conan create . demo/testing
```

When a packge is built a number of steps take place.

### export

Copy the conanfile to the local cache. The local cache, by default, is at ```~/.conan/data/```.
A subfolder for this package is created:

```
~/.conan/data/lib2
└── 0.1
    └── export
        ├── lib2
        │   ├── export
        │   │   ├── conanfile.py
        │   │   └── conanmanifest.txt
        │   └── export_source
        ├── lib2.count
        └── lib2.count.lock
```
### install

Installs the package (where?) forcing it to be builtfrom sources.

The local cache now becomes:

```
~/.conan/data/lib2
└── 0.1
    └── export
        ├── lib2
        │   ├── build
        │   │   └── f8bda7f0751e4bc3beaa6c3b2eb02d455291c8a2
...
        │   ├── export
        │   │   ├── conanfile.py
        │   │   └── conanmanifest.txt
        │   ├── export_source
...
        │   ├── package
        │   │   └── f8bda7f0751e4bc3beaa6c3b2eb02d455291c8a2
        │   │       ├── conaninfo.txt
        │   │       ├── conanmanifest.txt
        │   │       ├── include
        │   │       │   └── lib2.h
        │   │       └── lib
        │   │           └── liblib2.a
        │   └── source
        │       └── lib2
        │           ├── CMakeLists.txt
        │           ├── LICENSE
        │           ├── lib2.cpp
        │           ├── lib2.h
        │           └── lib2main.cpp
...
```
we see:
* the source directory
* the build directory for the current architecture (in this case, Mac OS X)
* the package directory

The package can be built for every combination of [ OS, Architecture, ...]. The hash value, ```f8bda7f0751e4bc3beaa6c3b2eb02d455291c8a2``` is actually the MD5 hash of the file ```??```.

### test

Build the test package (it will look in the ```test_package``` subfolder). Run the test package executable.

Consume Package
---------------

S

Distribute Packages
-------------------

The Tutorial
=

Creating lib2 package
-

The packages are created in a separate folder to the main source, [pkg](pkg)

```
$ conan new lib2/0.1 -t

Python 2 will soon be deprecated. It is strongly recommended to use Python 3 with Conan:
https://docs.conan.io/en/latest/installation.html#python-2-deprecation-notice

File saved: conanfile.py
File saved: test_package/CMakeLists.txt
File saved: test_package/conanfile.py
File saved: test_package/example.cpp
```
We can see that this has created a number of files to get us started creating a Conan package.

> By default, the conanfile.py is expecting to gather its sources from github repository above. The ```testpackage/example.cpp``` file is fixed to work with the example in this repository. 

The following is a stripped down version of the default conanfile.py.

```
from conans import ConanFile, CMake, tools

class Lib2Conan(ConanFile):
    name = "lib2"
    version = "0.1"
    ...

    def source(self):
        ...

    def build(self):
        ...

    def package(self):
        ...

    def package_info(self):
        ...
```
In the ```source```, we would like to get the source of the package from this repository. We can use an absolute URL for this.

```
    def source(self):
        self.run("cp -r /path/to/lib2 .")
        self.run("cd lib2")
```
> The example here is fragile with respect to changing the directory structure of the repository.

We can specify how the package is built in the ```build(self)``` method.

```
    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="lib2")
        cmake.build()
```
> Conan has classes to encapsulate building with CMake!

After the source is built we copy the artifacts into the package. The following code assumes packages are built on Mac OS X, Linux and Windows.

```
    def package(self):
        self.copy("*.h", dst="include", src="lib2")
        self.copy("*lib2.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)
```
> I thought Conan was meant to abstract platforms from the build process. Is there a better way of doing this??

Finally, we override the package_info method to specify the name of the library the consumers must link against.

```
    def package_info(self):
        self.cpp_info.libs = ["lib2"]
```

We can build the package using the ```conan create``` command.

```
$ conan create . export/lib2
```

Consuming lib2 package from lib1
-

To consume a package in another application or library we must specify the following:
* the packages we depend on
* the build system tools we are using in our current package.

In practice, we can do this by creating a file, ```conanfile.txt```, in the root of our application.
> Note: we are assuming that our application is built using CMake

```
[requires]
lib2/0.1@export/lib2

[generators]
cmake
```
Conan will help us create CMake file that includes all the necessary lib and header directives. To do this, we install the dependecies.

We make a build folder in the root of our lib2 source:

```
$ mkdir build && cd build
$ conan info ..
PROJECT
    ID: e519e80eca4c5a99fb54de4a0a5df2a62b42f4b4
    BuildID: None
    Requires:
        lib2/0.1@export/lib2
lib2/0.1@export/lib2
    ID: f8bda7f0751e4bc3beaa6c3b2eb02d455291c8a2
    BuildID: None
    Remote: None
    URL: <Package recipe repository url here, for issues about the package>
    License: <Put the package license here>
    Recipe: Cache
    Binary: Cache
    Binary remote: None
    Creation date: 2018-10-27 12:54:21
    Required by:
        PROJECT
```
We run ```conan install ..``` to generate a CMake include file to include in our existing cmake file.

```
$ conan install ..
Configuration:
[settings]
os=Macos
os_build=Macos
arch=x86_64
arch_build=x86_64
compiler=apple-clang
compiler.version=10.0
compiler.libcxx=libc++
build_type=Release
[options]
[build_requires]
[env]

PROJECT: Installing /Users/james/dev/conan-trial/lib1/conanfile.txt
Requirements
    lib2/0.1@export/lib2 from local cache - Cache
Packages
    lib2/0.1@export/lib2:f8bda7f0751e4bc3beaa6c3b2eb02d455291c8a2 - Cache

lib2/0.1@export/lib2: Already installed!
PROJECT: Generator cmake created conanbuildinfo.cmake
PROJECT: Generator txt created conanbuildinfo.txt
PROJECT: Generated conaninfo.txt
Jamess-Mac-mini:build james$ ls
conanbuildinfo.cmake    conanbuildinfo.txt      conaninfo.txt
```
We 'wire' our newly created ```conanbuildinfo.cmake``` file into our existing CMakeLists.txt file.

```
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
```
We can now generate our Makefiles and build our project.

```
$ cmake .. -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release
$ cmake --build .
```
> What does the ```-G``` option really specify??

We have now built a ```lib1``` library, but we have not created a lib1 Conan package.

Creating a lib1 package
-

Consuming lib1 package in app
-

Distributing packages
-

Building on different OS's
-






