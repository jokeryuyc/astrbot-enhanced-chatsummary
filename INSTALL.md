# AstrBot 增强版聊天总结插件安装指南

本文档提供了详细的插件安装步骤，适用于不同的环境和情况。

## Docker环境安装（推荐）

如果您使用Docker运行AstrBot，请按照以下步骤安装插件：

### 1. 进入Docker容器

```bash
docker exec -it 您的容器名称或ID bash
```

### 2. 安装Git（如果尚未安装）

```bash
apt-get update
apt-get install -y git
```

### 3. 克隆插件仓库

```bash
cd /tmp
git clone https://github.com/jokeryuyc/astrbot-enhanced-chatsummary.git
```

### 4. 安装插件

```bash
cd astrbot-enhanced-chatsummary
pip install -e .
```

### 5. 重启AstrBot服务

根据您的部署方式，重启AstrBot服务。

## 一键安装脚本

为了简化安装过程，我们提供了一键安装脚本：

```bash
curl -sSL https://raw.githubusercontent.com/jokeryuyc/astrbot-enhanced-chatsummary/main/install.sh | bash
```

## 手动安装（无Git环境）

如果您的环境中没有Git，或者无法使用Git，可以按照以下步骤进行手动安装：

1. 从GitHub下载ZIP源码包
2. 将ZIP文件上传到AstrBot服务器或Docker容器中
3. 解压文件：`unzip astrbot-enhanced-chatsummary.zip`
4. 进入目录：`cd astrbot-enhanced-chatsummary-main`
5. 安装插件：`pip install -e .`

## 验证安装

安装完成后，可以通过以下方式验证插件是否安装成功：

```bash
# 检查插件是否在已安装列表中
pip list | grep chatsummary

# 尝试使用插件命令
# 在您的聊天平台中输入: /消息总结 10
```

## 常见安装问题

### 问题1: pip安装失败

如果遇到以下错误：

```
ERROR: Could not find a version that satisfies the requirement astrbot-plugin-chatsummary
ERROR: No matching distribution found for astrbot-plugin-chatsummary
```

**解决方案**：
- 此插件尚未发布到PyPI，请使用源码安装方法而非直接pip安装
- 确保您使用的是正确的安装命令：`pip install -e .`（注意最后的点）
- 确保在正确的目录中执行安装命令（应在仓库根目录，包含setup.py文件的目录）

### 问题2: ImportError或ModuleNotFoundError

如果安装后使用时出现模块导入错误：

**解决方案**：
- 确保AstrBot版本兼容（>=0.1.0）
- 尝试使用确切的包名称安装：`pip install -e .`
- 检查Python环境路径是否正确

### 问题3: 权限问题

如果安装过程中遇到权限问题：

**解决方案**：
- 使用sudo或管理员权限安装（如适用）
- 检查文件夹权限，确保有写入权限

## 更多帮助

如果您在安装过程中遇到其他问题，请：

1. 查看项目的[Issue页面](https://github.com/jokeryuyc/astrbot-enhanced-chatsummary/issues)，看是否有类似问题
2. 创建新的Issue，详细描述您的问题和环境

我们会尽快为您提供支持。