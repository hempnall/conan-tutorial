from conans import ConanFile, CMake, tools


class Lib2Conan(ConanFile):
    name = "lib2"
    version = "0.1"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Lib2 here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        self.run("cp -r /Users/james/dev/conan-trial/lib2 .")
        self.run("cd lib2")

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="lib2")
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include", src="lib2")
        self.copy("*lib2.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["lib2"]

