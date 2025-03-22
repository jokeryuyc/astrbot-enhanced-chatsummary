# 贡献指南

感谢您考虑为 AstrBot 增强版聊天总结插件做出贡献！这个文档提供了贡献代码的指南和流程说明。

## 开发环境设置

1. Fork 本仓库到您的GitHub账户
2. 克隆您fork的仓库到本地：
   ```bash
   git clone https://github.com/YOUR_USERNAME/astrbot-enhanced-chatsummary.git
   ```
3. 添加上游仓库：
   ```bash
   git remote add upstream https://github.com/jokeryuyc/astrbot-enhanced-chatsummary.git
   ```
4. 创建并切换到新的分支：
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 代码风格指南

本项目遵循以下代码风格规范：

- 使用4个空格缩进
- 函数和类应有清晰的文档字符串(docstring)
- 变量和函数使用snake_case命名
- 类使用CamelCase命名
- 保持代码简洁，函数不超过50行
- 添加适当的注释解释复杂逻辑

## 提交Pull Request流程

1. 确保您的代码通过所有测试
2. 更新相关文档
3. 推送您的分支到您的fork仓库：
   ```bash
   git push origin feature/your-feature-name
   ```
4. 通过GitHub界面创建Pull Request到主仓库的main分支
5. 在PR描述中清晰说明您的更改内容和目的
6. 等待审核和反馈

## 分支策略

- `main`: 生产就绪的稳定代码
- `develop`: 开发分支，合并功能分支
- `feature/*`: 新功能开发
- `bugfix/*`: 修复bug
- `docs/*`: 文档更新

## 版本发布

本项目使用语义化版本管理(SemVer)：

- 主版本号(X.0.0)：不兼容的API变更
- 次版本号(X.Y.0)：向后兼容的功能性新增
- 修订号(X.Y.Z)：向后兼容的问题修正

## 问题报告

如果您发现bug或有功能建议，请创建新的Issue，并提供以下信息：

- 详细的问题描述
- 复现步骤
- 预期行为和实际行为
- 截图（如适用）
- 环境信息（AstrBot版本、操作系统等）

## 代码审核

所有的PR将由维护者审核。审核标准包括：

- 代码质量和风格
- 测试覆盖率
- 文档完整性
- 功能实现是否符合项目目标

## 行为准则

请尊重所有贡献者和用户。讨论应保持友善和建设性。不当行为将导致贡献被拒绝。

## 许可证

通过提交代码，您同意您的贡献将在项目的AGPL-3.0许可下发布。