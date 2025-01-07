cmake_minimum_required(VERSION 3.21)
project(AetherEngine LANGUAGES CXX)

# 设置 C++ 标准
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 可选构建测试
option(BUILD_TESTS "Build tests" OFF)

# 加载子模块
add_subdirectory(src)

# 如果启用了测试，加载测试目录
if(BUILD_TESTS)
    enable_testing()
    add_subdirectory(tests)
endif()
