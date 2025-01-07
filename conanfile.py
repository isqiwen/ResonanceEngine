from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.files import copy
import os

class AetherEngineConan(ConanFile):
    name = "aether_engine"
    version = "1.0.0"

    # Optional metadata
    license = "<Put the package license here>"
    author = "<Put your name here> <And your email here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of hello package here>"
    topics = ("<Put some tag here>", "<here>", "<and here>")

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {
        "shared": False,
        "fPIC": True,
        "assimp/*:shared": False,
        "bullet3/*:shared": False,
        "spdlog/*:header_only": True,
    }

    exports_sources = "CMakeLists.txt", "src/*", "include/*"

    # 主工程依赖
    requires = [
        "glfw/3.3.8",          # 窗口管理
        "assimp/5.2.5",        # 模型加载
        "bullet3/3.25",        # 物理引擎
        "spdlog/1.11.0",       # 日志系统
        "freetype/2.12.1",     # 字体渲染
    ]

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def layout(self):
        cmake_layout(self)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["aether_engine"]
