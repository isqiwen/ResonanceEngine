import sys
from pathlib import Path

from .config_loader import ConfigLoader

PYTHON_BUILD_MODULE_ROOT = Path(__file__).resolve().parent
PYTHON_MODULE_ROOT = PYTHON_BUILD_MODULE_ROOT.parent
PYTHON_CONFIG_MODULE_ROOT = PYTHON_MODULE_ROOT / "config"
PYTHON_COMMON_MODULE_ROOT = PYTHON_MODULE_ROOT / "common"
TOOLS_ROOT = PYTHON_MODULE_ROOT.parent
PROJECT_ROOT = TOOLS_ROOT.parent

def AddPathToModuleSearchPath(module_path):
    p = str(module_path)
    if p not in sys.path:
        sys.path.insert(0, p)

def IncludePackage():
    AddPathToModuleSearchPath(PYTHON_MODULE_ROOT)

IncludePackage()

from common.platform_utils import Platform
from common.logger_config import Logger

BUILD_CONFIG_PATH = PYTHON_CONFIG_MODULE_ROOT / "build_config.json"
CONFIG = ConfigLoader(BUILD_CONFIG_PATH)

PROJECT_NAME = CONFIG.get("global.project_name")
PLATFORM = Platform.detect()
BUILD_DIR = PROJECT_ROOT / CONFIG.get(f"platforms.{PLATFORM}.build_dir")
INSTALL_DIR = PROJECT_ROOT / CONFIG.get(f"platforms.{PLATFORM}.install_dir")
DIST_DIR = PROJECT_ROOT / CONFIG.get(f"platforms.{PLATFORM}.dist_dir")

CMAKE_FLAGS = CONFIG.get(f"platforms.{PLATFORM}.cmake_flags")
ENV_VARS = CONFIG.get(f"platforms.{PLATFORM}.env")
CPP_CMAKE_GEN_TARGET = CONFIG.get(f"platforms.{PLATFORM}.cpp_cmake_gen_target")

conan_user_home_template = CONFIG.get(f"global.conan.user_home.{PLATFORM}")
CONAN_USER_HOME = conan_user_home_template.format(project_name=PROJECT_NAME)
CONAN_USER_HOME= Path(PROJECT_ROOT.drive) / CONAN_USER_HOME if Platform.is_windows() else CONAN_USER_HOME

bin_prefix = 'Scripts' if Platform.is_windows() else 'bin'
bin_suffix = '.exe' if Platform.is_windows() else ''
CONAN_EXE = PROJECT_ROOT / ".venv" / bin_prefix / ("conan" + bin_suffix)
CONAN_PROFILE_NAME = "vs19_and_cppstd17" if Platform.is_windows() else "gcc9_and_cppstd17"
CONAN_PROFILE_CONTENT = CONFIG.get(f"global.conan.profiles.vs19_and_cppstd17") if Platform.is_windows() else CONFIG.get(f"global.conan.profiles.gcc9_and_cppstd17")

def log_configuration():
    Logger.Info('Config: ################################################################################')
    Logger.Info(f'Config: {PROJECT_NAME} Project Paths')
    Logger.Info(f'Config:    Project Root                               = {PROJECT_ROOT}')
    Logger.Info(f'Config:    Tools Root                                 = {TOOLS_ROOT}')
    Logger.Info(f'Config:    Python Tools Module Root                   = {PYTHON_MODULE_ROOT}')
    Logger.Info(f'Config:    Python Tools Build Module Root             = {PYTHON_BUILD_MODULE_ROOT}')
    Logger.Info(f'Config:    Python Tools Common Module Root            = {PYTHON_COMMON_MODULE_ROOT}')
    Logger.Info(f'Config:    Python Tools Config Module Root            = {PYTHON_CONFIG_MODULE_ROOT}')
    Logger.Info(f"Config:    Conan                                      = {CONAN_EXE}")
    Logger.Info(f"Config:    Conan User Home                            = {CONAN_USER_HOME}")
    Logger.Info(f"Config:    Build Directory                            = {BUILD_DIR}")
    Logger.Info(f"Config:    Install Directory                          = {INSTALL_DIR}")
    Logger.Info(f"Config:    Distribution Directory                     = {DIST_DIR}")
    Logger.Info(f"Config:    CMake Flags                                = {CMAKE_FLAGS}")
    Logger.Info(f"Config:    Environment Variables                      = {ENV_VARS}")
    Logger.Info('Config: ################################################################################')
