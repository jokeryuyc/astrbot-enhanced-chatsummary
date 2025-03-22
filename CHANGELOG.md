# 更新日志

所有对项目的显著更改都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
并且本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [1.0.2] - 2025-03-22

### 修复
- 修复了DeepSeek Reasoner LLM调用格式问题，现在使用正确的系统消息+用户消息格式
- 修复了文件读取时可能出现的编码问题
- 修复了缺少错误处理的潜在崩溃问题

### 新增
- 添加了对更多消息类型的支持（图片、文件、语音、@消息等）
- 添加了最大记录数限制（默认300条），防止请求过大
- 添加了详细的类型注解和文档字符串
- 增强了调试模式，提供更多调试信息

### 变更
- 重构代码结构，将功能模块化为独立函数
- 改进错误处理，添加更友好的用户错误提示
- 更新文档和配置说明，提供更详细的使用指南
- 优化长文本处理，避免消息溢出问题

## [1.0.1] - 2024-12-15

### 新增
- 初始版本发布
- 基本的群聊消息总结功能
- 支持文本和表情消息处理
- 提供基础提示词配置

[1.0.2]: https://github.com/jokeryuyc/astrbot-enhanced-chatsummary/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/jokeryuyc/astrbot-enhanced-chatsummary/releases/tag/v1.0.1
