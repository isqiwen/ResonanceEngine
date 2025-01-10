#pragma once

#include <fstream>
#include <string>
#include <vector>
#include <memory>
#include <spdlog/spdlog.h>
#include <spdlog/sinks/stdout_color_sinks.h>
#include <spdlog/sinks/rotating_file_sink.h>
#include <spdlog/async.h>
#include <spdlog/async_logger.h>

namespace Aether::Core {

    class Logger {
    public:
        static void Init();
    };

}
