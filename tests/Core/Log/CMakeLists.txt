# Logger 测试文件
set(LOGGER_TEST_SRC
    TestLogger.cpp
)

# 添加到测试目标
target_sources(AetherEngineTests PRIVATE ${LOGGER_TEST_SRC})
target_include_directories(AetherEngineTests PRIVATE ../../src/Core/Logger)
