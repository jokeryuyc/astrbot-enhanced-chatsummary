#!/bin/bash
# install.sh - AstrBot 聊天总结插件一键安装脚本

echo "开始安装 AstrBot 聊天总结插件..."

# 检查是否在Docker环境中
if [ -f /.dockerenv ]; then
    echo "检测到Docker环境"
else
    echo "警告：未检测到Docker环境，请确保您在AstrBot的Docker容器中运行此脚本"
    echo "继续安装? (y/n)"
    read -r continue_install
    if [ "$continue_install" != "y" ]; then
        echo "安装已取消"
        exit 1
    fi
fi

# 安装git（如果需要）
if ! command -v git &> /dev/null; then
    echo "正在安装git..."
    apt-get update && apt-get install -y git
fi

# 克隆仓库
echo "正在克隆插件仓库..."
mkdir -p /tmp
cd /tmp || exit
if [ -d "astrbot-enhanced-chatsummary" ]; then
    echo "检测到已有仓库，正在更新..."
    cd astrbot-enhanced-chatsummary || exit
    git pull
else
    git clone https://github.com/jokeryuyc/astrbot-enhanced-chatsummary.git
    cd astrbot-enhanced-chatsummary || exit
fi

# 安装插件
echo "正在安装插件..."
pip install -e .

# 检查安装结果
if pip list | grep -q "astrbot-plugin-chatsummary"; then
    echo "✅ 安装成功！"
    echo "请重启AstrBot以激活插件。"
    echo "使用方法: /消息总结 100"
else
    echo "❌ 安装似乎失败，请检查错误信息。"
    echo "您可以尝试手动安装:"
    echo "cd /tmp/astrbot-enhanced-chatsummary && pip install -e ."
fi