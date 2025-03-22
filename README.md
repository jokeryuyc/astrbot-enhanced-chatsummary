
# AstrBot 增强版聊天总结插件

一个基于LLM的智能历史聊天记录总结插件，支持结构化输出和自定义提示词。

## 功能特点

- 🚀 **智能总结**：使用大型语言模型分析群聊记录，提取关键信息
- 📊 **结构化输出**：清晰的分类，包括「今日速览」、「热门话题」等板块
- 🔍 **多消息类型支持**：处理文本、表情、图片、文件、语音和@消息等
- ⚙️ **高度可定制**：自定义提示词和输出格式
- 🛡️ **稳定可靠**：完善的错误处理机制
- 🧩 **模块化设计**：代码结构清晰，易于扩展

## 使用方法

### 基本命令

```
/消息总结 100         # 总结最近100条消息
/消息总结 50 debug    # 调试模式(仅管理员)
```

### 示例输出

```
【今日速览】
今天群里热闹非凡！大家讨论了项目进度、技术选型，还分享了不少有趣的见闻和创意。

【热门话题】
· 技术架构升级方案 
  - 团队正在从单体架构迁移到微服务架构
  - 已确定使用Kubernetes作为容器编排工具

【趣味时刻】
· 「老张」分享了一个程序员加班的表情包，引发大家集体"泪目" 😂

【群聊温度计】
今天的群聊氛围非常积极向上，技术讨论有深度，日常互动有温度。💯
```

## 安装方法

### 方法一：直接从GitHub安装（推荐）

```bash
# 进入Docker终端
docker exec -it your_astrbot_container bash

# 克隆仓库
git clone https://github.com/jokeryuyc/astrbot-enhanced-chatsummary.git

# 安装
cd astrbot-enhanced-chatsummary
pip install -e .
```

### 方法二：下载源码安装

如果无法使用git，可以下载ZIP源码包后上传到Docker容器中：

```bash
# 在容器中
cd /tmp
# 解压下载的zip文件
unzip astrbot-enhanced-chatsummary.zip
cd astrbot-enhanced-chatsummary
pip install -e .
```

### 方法三：使用一键安装脚本

```bash
# 进入Docker终端
docker exec -it your_astrbot_container bash

# 下载并执行安装脚本
curl -sSL https://raw.githubusercontent.com/jokeryuyc/astrbot-enhanced-chatsummary/main/install.sh | bash
```

## 配置选项

插件支持以下配置项目：

| 配置项 | 描述 | 默认值 |
|--------|------|--------|
| prompt | LLM提示词，控制总结风格 | 详见config_schema.json |
| max_records | 最大支持总结的记录数 | 300 |
| extract_image_text | 是否提取图片内容 | false |
| debug_mode | 调试模式设置 | 默认关闭 |

## 常见问题

### 问题：无法通过pip安装

错误信息: `ERROR: Could not find a version that satisfies the requirement astrbot-plugin-chatsummary`

**解决方案**：
- 目前插件尚未发布到PyPI，请使用源码安装方法
- 确保使用的是最新版本的AstrBot(>=0.1.0)
- 检查网络连接是否正常

### 问题：安装后无法使用

**解决方案**：
- 确认插件已正确安装: `pip list | grep chatsummary`
- 检查AstrBot的插件目录中是否有相关配置
- 重启AstrBot服务: `systemctl restart astrbot` 或相应的重启命令

### 问题：提示缺少依赖

**解决方案**：
- 手动安装依赖: `pip install -r requirements.txt`
- 如果在Docker环境中，确保容器有网络连接

## 版本历史

### [1.0.3] - 开发中
- 优化输出效果和兼容性
- 改进多平台支持

### [1.0.2] - 2025-03-22
- 修复DeepSeek Reasoner LLM调用格式问题
- 添加更多消息类型支持
- 增加最大记录数限制
- 添加详细文档

### [1.0.1] - 2024-12-15
- 初始版本发布
- 基本的群聊消息总结功能

## 贡献指南

欢迎提交Pull Request或Issue！

## 许可证

本项目采用 [AGPL-3.0](LICENSE) 许可证。

## 致谢

本项目基于 [laopanmemz/astrbot_plugin_chatsummary](https://github.com/laopanmemz/astrbot_plugin_chatsummary) 开发，感谢原作者的工作和灵感。此增强版本在原有基础上添加了更多功能和优化，包括:
- 更丰富的消息类型支持
- 改进的错误处理机制
- 优化的代码结构
- 详细的安装文档和脚本
