# Logger 模块

find_package(spdlog REQUIRED)

set(LOGGER_SRC
    Logger.cpp
    Logger.h
)

add_library(Logger STATIC ${LOGGER_SRC})
target_include_directories(Logger PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(Logger PRIVATE spdlog::spdlog_header_only)
