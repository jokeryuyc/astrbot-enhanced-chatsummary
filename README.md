# AstrBot 增强版聊天总结插件

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/jokeryuyc/astrbot-enhanced-chatsummary/ci.yml?branch=main)
![Python Versions](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10-blue)
![License](https://img.shields.io/github/license/jokeryuyc/astrbot-enhanced-chatsummary)
![Version](https://img.shields.io/badge/version-1.0.3-green)

一个基于LLM的智能历史聊天记录总结插件，支持结构化输出和自定义提示词。**本项目基于 [laopanmemz/astrbot_plugin_chatsummary](https://github.com/laopanmemz/astrbot_plugin_chatsummary) 进行功能增强和兼容性扩展开发**。

## 🌟 功能特点

- 🚀 **智能总结**：使用大型语言模型分析群聊记录，提取关键信息
- 📊 **结构化输出**：清晰的分类，包括「今日速览」、「热门话题」等板块
- 🔍 **多消息类型支持**：处理文本、表情、图片、文件、语音和@消息等
- ⚙️ **高度可定制**：自定义提示词和输出格式
- 🛡️ **稳定可靠**：完善的错误处理机制
- 🧩 **模块化设计**：代码结构清晰，易于扩展
- 🌍 **国际化支持**：支持多语言界面和提示

## 📋 使用方法

在聊天中输入以下命令触发消息总结：

```
/消息总结 [数量]
```

例如：`/消息总结 100` 将总结最近 100 条消息。

管理员可以使用调试模式：`/消息总结 100 debug`

## 🔧 安装指南

### 推荐安装方式（本地开发）

```bash
git clone https://github.com/jokeryuyc/astrbot-enhanced-chatsummary.git
cd astrbot-enhanced-chatsummary
pip install -e .
```

### 一键安装脚本

```bash
curl -sSL https://raw.githubusercontent.com/jokeryuyc/astrbot-enhanced-chatsummary/main/install.sh | bash
```

更多安装选项和常见问题解答，请查看 [INSTALL.md](INSTALL.md)。

## 📝 配置说明

插件提供了多种配置选项，可以在 `data/config/` 目录下的配置文件中进行调整：

- **模板设置**：修改输出格式和样式
- **提示词设置**：自定义发送给LLM的提示词
- **行为设置**：调整插件的工作方式和触发条件

详细配置说明请参考 [docs/CONFIG.md](docs/CONFIG.md)。

## 🔄 平台兼容性

本插件支持以下平台：

- ✅ **QQ**
- ✅ **微信**
- ✅ **钉钉**
- ✅ **飞书**

详细的平台适配指南和特性说明请参考 [docs/PLATFORM_COMPATIBILITY.md](docs/PLATFORM_COMPATIBILITY.md)。

## 源项目与增强功能对比

本项目在原始 [astrbot_plugin_chatsummary](https://github.com/laopanmemz/astrbot_plugin_chatsummary) 基础上进行了多项增强与扩展：

| 功能 | 原始插件 | 增强版 | 详细说明 |
|-----|---------|-------|----------|
| **多平台支持** | 有限支持 | ✅ 全面支持 | 新增微信、钉钉、飞书等平台适配 |
| **国际化** | ❌ | ✅ | 支持中英日等多种语言界面和提示 |
| **错误处理** | 基础 | ✅ 增强 | 新增全面的异常捕获和恢复机制 |
| **安装方式** | 单一 | ✅ 多样化 | 增加一键安装脚本、Docker支持等 |
| **文档完善** | 基础说明 | ✅ 专业文档 | 新增安装指南、排错手册、API文档等 |
| **测试覆盖** | 有限 | ✅ 全面 | 增加单元测试和CI/CD流程 |
| **社区支持** | 基础 | ✅ 活跃 | 新增贡献指南和问题模板 |

## 🤝 贡献指南

欢迎贡献代码、提交问题或改进建议！请参阅 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

## 📜 更新日志

查看 [CHANGELOG.md](CHANGELOG.md) 了解版本更新历史。

## 📄 许可证

本项目采用 MIT 许可证 - 详情请参阅 [LICENSE](LICENSE) 文件。

## 🙏 致谢

特别感谢 [laopanmemz](https://github.com/laopanmemz) 提供的原始插件代码 **astrbot_plugin_chatsummary**，此项目为本增强版提供了坚实的功能基础和架构灵感。本项目在保留原始核心功能的基础上，进行了多方面的增强和扩展，包括多平台兼容性、错误处理机制和用户体验优化等。

同时感谢所有为项目做出贡献的开发者和测试人员，你们的支持对项目的完善至关重要。