#include <gtest/gtest.h>

#include "Logger/Logger.h"

TEST(Logger, Initialization) {
    Logger::Init();
    EXPECT_NE(Logger::GetConsoleLogger(), nullptr);
    EXPECT_NE(Logger::GetFileLogger(), nullptr);
}

TEST(Logger, LogMessages) {
    Logger::Init();
    EXPECT_NO_THROW(Logger::GetConsoleLogger()->info("Test log message"));
}
