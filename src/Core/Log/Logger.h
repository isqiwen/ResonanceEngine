#pragma once

#include <memory>
#include <spdlog/spdlog.h>
#include <spdlog/sinks/stdout_color_sinks.h>
#include <spdlog/sinks/basic_file_sink.h>

namespace Aether::Core {

    class Logger {
    public:
        static void Init();
    };

}
