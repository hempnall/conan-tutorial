from conans import ConanFile, CMake, tools


class Lib1Conan(ConanFile):
    name = "lib1"
    version = "0.2"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Lib1 here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    build_requires = "lib2/[>=0.2]@export/lib2"
    requires = "lib2/[>=0.2]@export/lib2"

    def source(self):
        self.run("git clone https://github.com/hempnall/conan-tutorial.git")
        self.run("cd conan-tutorial/lib1")

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="conan-tutorial/lib1")
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include", src="conan-tutorial/lib1")
        self.copy("*hello.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["lib1"]

