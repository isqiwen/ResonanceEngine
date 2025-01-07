#!/bin/bash
set -e

# 检查是否提供环境名称参数
if [ -z "$1" ]; then
    echo "Usage: ./setup_conan_env_conda.sh <env_name>"
    exit 1
fi

# 读取环境名称
ENV_NAME="$1"

# 检查 Conda 是否可用
if ! command -v conda &> /dev/null; then
    echo "Conda is not installed or not in PATH. Please install Conda first."
    exit 1
fi

# 创建 Conda 环境
echo "Creating Conda environment: $ENV_NAME..."
conda create -n "$ENV_NAME" python=3.10 -y

# 激活环境
echo "Activating Conda environment: $ENV_NAME..."
conda activate "$ENV_NAME"

# 安装 Conan
echo "Installing Conan via Conda..."
conda install -c conan -c conda-forge conan -y

# 设置 Conan 镜像源
echo "Setting Tsinghua mirror for Conan..."
conan config set general.revisions_enabled=1
conan config set general.default_profile=default
conan config install https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/

# 检查并创建默认 Profile
if ! conan profile show default &> /dev/null; then
    echo "Creating default Conan profile..."
    conan profile detect
fi

# 更新默认 Profile 配置
echo "Updating default profile settings..."
conan profile update settings.compiler.cppstd=17 default
conan profile update settings.build_type=Release default
conan profile update settings.arch=x86_64 default

# 完成
echo "Conda-based Conan environment setup for $ENV_NAME complete."
