# 顶层测试 CMake 文件
add_subdirectory(Core)

# 创建测试目标
add_executable(AetherEngineTests)

# 链接测试目标到主引擎库和测试框架
target_link_libraries(AetherEngineTests PRIVATE AetherEngine gtest_main)

# 自动发现并运行测试
include(GoogleTest)
gtest_discover_tests(AetherEngineTests)
