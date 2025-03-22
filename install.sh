#!/bin/bash

# AstrBot 增强版聊天总结插件安装脚本
# 版本: 1.0.3
# 作者: jokeryuyc

set -e

# 颜色输出函数
RED="\033[0;31m"
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
BLUE="\033[0;34m"
RESET="\033[0m"

info() {
    echo -e "${BLUE}[INFO]${RESET} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${RESET} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${RESET} $1"
}

error() {
    echo -e "${RED}[ERROR]${RESET} $1"
}

# 检查必要的命令
check_command() {
    if ! command -v $1 &> /dev/null; then
        error "$1 命令未找到，请先安装它"
        return 1
    fi
}

# 判断方式函数
get_install_method() {
    # 检查是否在Docker环境中
    if [ -f /.dockerenv ] || grep -q docker /proc/self/cgroup 2>/dev/null; then
        echo "docker"
        return
    fi
    
    # 检查是否有Git
    if command -v git &> /dev/null; then
        echo "git"
        return
    fi
    
    # 默认使用ZIP下载方式
    echo "zip"
}

# 创建临时目录
setup_temp_dir() {
    TMP_DIR=$(mktemp -d)
    info "创建临时目录: $TMP_DIR"
    # 确保退出时清理
    trap "rm -rf $TMP_DIR" EXIT
}

# Git安装方式
git_install() {
    info "使用Git方式安装"
    
    cd "$TMP_DIR"
    info "克隆仓库..."
    git clone https://github.com/jokeryuyc/astrbot-enhanced-chatsummary.git
    
    cd astrbot-enhanced-chatsummary
    info "开始安装依赖..."
    pip install -e . --no-deps
    pip install -r requirements.txt
    
    success "使用Git方式安装成功"
}

# 下载ZIP方式安装
zip_install() {
    info "使用ZIP方式安装"
    
    cd "$TMP_DIR"
    info "下载源码压缩包..."
    curl -L -o plugin.zip "https://github.com/jokeryuyc/astrbot-enhanced-chatsummary/archive/refs/heads/main.zip"
    
    info "解压缩中..."
    unzip -q plugin.zip
    cd astrbot-enhanced-chatsummary-main
    
    info "开始安装依赖..."
    pip install -e . --no-deps
    pip install -r requirements.txt
    
    success "使用ZIP方式安装成功"
}

# Docker安装方式
docker_install() {
    info "检测到Docker环境，使用容器内安装方式"
    
    # 检查容器中是否有git
    if command -v git &> /dev/null; then
        git_install
    else
        warning "Docker环境中无Git，尝试安装Git"
        apt-get update -qq && apt-get install -y git curl unzip > /dev/null 2>&1 || {
            warning "Git安装失败，切换到ZIP方式"
            zip_install
        }
        
        # 再次尝试Git安装
        if command -v git &> /dev/null; then
            git_install
        else
            zip_install
        fi
    fi
}

# 验证安装
verify_installation() {
    info "验证安装..."
    
    # 检查包是否安装成功
    if pip list | grep -q astrbot-plugin-chatsummary; then
        success "插件已成功安装! 可使用 '/消息总结' 命令进行测试"
    else
        error "插件安装失败，请查看上面的错误信息"
        exit 1
    fi
    
    # 检查配置文件
    if [ -d "$TMP_DIR/astrbot-enhanced-chatsummary" ]; then
        CONFIG_DIR="$TMP_DIR/astrbot-enhanced-chatsummary/data/config"
    elif [ -d "$TMP_DIR/astrbot-enhanced-chatsummary-main" ]; then
        CONFIG_DIR="$TMP_DIR/astrbot-enhanced-chatsummary-main/data/config"
    fi
    
    if [ -d "$CONFIG_DIR" ]; then
        info "配置文件位于: $CONFIG_DIR"
    else
        warning "未找到配置目录，插件可能需要手动配置"
    fi
    
    echo -e "\n-----------------------------"
    echo -e "${GREEN}安装完成!${RESET}"
    echo -e "\n使用方法:"
    echo -e "  - 在聊天中输入 ${BLUE}/消息总结 100${RESET} 来总结最近100条消息"
    echo -e "  - 管理员可使用 ${BLUE}/消息总结 100 debug${RESET} 来查看调试信息"
    echo -e "\n有关更多信息，请访问: https://github.com/jokeryuyc/astrbot-enhanced-chatsummary"
    echo -e "-----------------------------\n"
}

# 组件安装检查
check_prerequisites() {
    info "检查必要组件..."
    
    # 检查 Python
    if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
        error "Python 未安装，请先安装 Python 3.8 或更高版本"
        exit 1
    fi
    
    # 检查 pip
    if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
        error "pip 未安装，请先安装 pip"
        exit 1
    fi
    
    # 确定PIP命令
    if command -v pip3 &> /dev/null; then
        PIP_CMD="pip3"
    else
        PIP_CMD="pip"
    fi
    
    # 升级 pip
    info "升级 pip..."
    $PIP_CMD install --upgrade pip -q
    
    success "基础组件检查完成"
}

# 主函数
main() {
    echo -e "\n${BLUE}==============================${RESET}"
    echo -e "${GREEN}AstrBot 增强版聊天总结插件安装脚本${RESET}"
    echo -e "${BLUE}==============================${RESET}\n"
    
    # 检查必要组件
    check_prerequisites
    
    # 创建临时目录
    setup_temp_dir
    
    # 确定安装方式
    INSTALL_METHOD=$(get_install_method)
    info "选择安装方式: $INSTALL_METHOD"
    
    # 执行安装
    case $INSTALL_METHOD in
        git)
            git_install
            ;;
        docker)
            docker_install
            ;;
        zip)
            zip_install
            ;;
        *)
            error "未知的安装方式"
            exit 1
            ;;
    esac
    
    # 验证安装
    verify_installation
}

# 执行主函数
main "$@"
