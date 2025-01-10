import os
import sys
import shutil
from pathlib import Path

from common.platform_utils import Platform
from common.shell_utils import run_command
from common.logger_config import Logger


def get_cmake_exe(conan_toolchain_file):
    try:
        if not os.path.exists(conan_toolchain_file):
            raise FileNotFoundError(f"Toolchain file not found: {conan_toolchain_file}")

        with open(conan_toolchain_file, "r") as file:
            for line in file:
                if "CMAKE_PROGRAM" in line:
                    cmake_path = Path(line.split('"')[1])
                    Logger.Info(f"Conan-installed CMake path: {cmake_path}")

                    if Platform.is_windows():
                        return cmake_path / "cmake.exe"
                    else:
                        return cmake_path / "cmake"
    except Exception as e:
        Logger.Info(f"Error reading toolchain file: {e}")
        return None


def get_cpp_cmake_gen_target():
    """
    Automatically detect the appropriate CMake generator based on the system and available tools.
    """
    if Platform.is_windows():
        vs_generators = [
            '"Visual Studio 17 2022"',
            '"Visual Studio 16 2019"'
        ]
        for generator in vs_generators:
            if is_cmake_generator_available(generator):
                return generator

        # Fallback to Ninja if Visual Studio is not available
        if is_ninja_available():
            return "Ninja"

        raise Exception("No suitable CMake generator found on Windows.")
    elif Platform.is_unix_like():
        # Prefer Ninja if available
        if is_ninja_available():
            return "Ninja"

        # Fallback to Makefiles
        if is_cmake_generator_available("Unix Makefiles"):
            return "Unix Makefiles"

        raise Exception("No suitable CMake generator found on Unix.")
    else:
        raise Exception(f"Unsupported system type: {sys.platform}")


def is_cmake_generator_available(generator):
    """
    Check if the given CMake generator is available on the system.
    """
    try:
        success, _, _ = run_command(["cmake", "-G", generator, "--version"], check=False)
        return success
    except FileNotFoundError:
        return False


def is_ninja_available():
    """
    Check if Ninja is installed and available in PATH.
    """
    return shutil.which("ninja") is not None


if __name__ == "__main__":
    try:
        generator = get_cpp_cmake_gen_target()
        Logger.Info(f"Detected CMake generator: {generator}")
    except Exception as e:
        Logger.Info(f"Error: {e}")
