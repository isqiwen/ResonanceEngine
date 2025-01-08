import os
import shutil
import subprocess
import sys

# 构建目录基础路径
BUILD_BASE_DIR = "build"

def run_command(cmd):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        raise Exception(f"Command failed: {cmd}")

def clean(build_type):
    """
    删除构建目录
    """
    build_dir = os.path.join(BUILD_BASE_DIR, build_type.lower())
    if os.path.exists(build_dir):
        print(f"Cleaning build directory: {build_dir}")
        shutil.rmtree(build_dir)
    else:
        print(f"Build directory does not exist: {build_dir}")

def build(build_type):
    """
    执行构建流程
    """
    build_dir = os.path.join(BUILD_BASE_DIR, build_type.lower())
    os.makedirs(build_dir, exist_ok=True)

    # 安装依赖
    run_command(
        f"conan install . --output-folder={build_dir} --build=missing -s build_type={build_type}"
    )

    # 配置 CMake
    toolchain_file = os.path.join(build_dir, "generators", "conan_toolchain.cmake")
    run_command(
        f"cmake -S . -B {build_dir} -DCMAKE_TOOLCHAIN_FILE={toolchain_file} -DCMAKE_BUILD_TYPE={build_type}"
    )

    # 构建项目
    run_command(f"cmake --build {build_dir}")

def main():
    """
    主流程
    """
    if len(sys.argv) != 3 or sys.argv[1] not in {"build", "clean"} or sys.argv[2] not in {"Release", "Debug"}:
        print("Usage: python build.py <build|clean> <Release|Debug>")
        sys.exit(1)

    action = sys.argv[1]
    build_type = sys.argv[2]

    if action == "clean":
        clean(build_type)
    elif action == "build":
        build(build_type)

if __name__ == "__main__":
    main()
