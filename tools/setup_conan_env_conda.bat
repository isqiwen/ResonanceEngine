@echo off

chcp 65001

setlocal enabledelayedexpansion enableextensions

setlocal

:: 检查是否提供环境名称参数

echo Step: Conda check...
conda --version

if "%1"=="" (
    echo "Usage: setup_conan_env_conda.bat <env_name>"
    exit /b 1
)

:: 读取环境名称
set ENV_NAME=%1

:: 检查 Conda 是否可用
conda --version >nul 2>&1
if %errorlevel% neq 0 (
    echo "Conda is not installed or not in PATH. Please install Conda first."
    exit /b 1
)

:: 创建 Conda 环境
echo Creating Conda environment: %ENV_NAME%...
conda create -n %ENV_NAME% python=3.10 -y

:: 激活环境
call conda activate %ENV_NAME%

:: 安装 Conan
echo Installing Conan via Conda...
conda install -c conan -c conda-forge conan -y

:: 设置 Conan 镜像源
echo Setting Tsinghua mirror for Conan...
conan config set general.revisions_enabled=1
conan config set general.default_profile=default
conan config install https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/

:: 检查并创建默认 Profile
conan profile show default >nul 2>&1
if %errorlevel% neq 0 (
    echo "Creating default Conan profile..."
    conan profile detect
)

:: 更新默认 Profile 配置
echo Updating default profile settings...
conan profile update settings.compiler.cppstd=17 default
conan profile update settings.build_type=Release default
conan profile update settings.arch=x86_64 default

:: 完成
echo "Conda-based Conan environment setup for %ENV_NAME% complete."
pause

endlocal
