# 开发指南

本文档提供了 AstrBot 增强版聊天总结插件的开发指南。

## 环境要求

- Python 3.10+
- AstrBot 0.1.0+

## 代码结构

```
.
├── data/                 # 数据文件夹
│   └── config/          # 配置文件
├── docs/                 # 文档
├── i18n/                 # 国际化文件
├── tests/                # 测试文件
├── .github/              # GitHub网站相关文件
├── main.py               # 主程序
├── metadata.yaml         # 元数据
├── setup.py              # 安装脚本
├── README.md             # 项目说明
├── README_en.md          # 英文项目说明
├── INSTALL.md            # 安装指南
├── CONTRIBUTING.md        # 贡献指南
├── LICENSE                # 许可证
└── .gitignore            # Git忽略文件
```

## 主要组件

### main.py

主要类是 `ChatSummary`，它继承自 `Star` 类，包含以下主要方法：

1. `summary`: 处理消息总结命令
2. `_fetch_group_messages`: 获取群组历史消息
3. `_extract_message_text`: 从消息段中提取文本
4. `_generate_summary`: 生成聊天总结
5. `_load_prompt`: 加载提示词
6. `_is_admin`: 检查用户是否为管理员

### i18n

国际化支持目录，主要包含：

1. `__init__.py`: 国际化核心代码
2. `zh_CN.json`: 中文翻译
3. `en_US.json`: 英文翻译

## 开发流程

### 1. 新功能开发

1. 创建新的功能分支
```bash
git checkout -b feature/your-feature-name
```

2. 在 `main.py` 或相关文件中实现功能

3. 添加相应的测试
```bash
python -m unittest tests.test_chatsummary
```

4. 更新文档

5. 提交变更
```bash
git add .
git commit -m "feat: add your feature description"
git push origin feature/your-feature-name
```

6. 创建PR到main分支

### 2. 国际化支持

要使用国际化功能，请在代码中如下使用：

```python
from i18n import get as _

# 使用翻译
message = _("summary_no_count")

# 带参数的翻译
message = _("summary_too_many", max_count=300)
```

### 3. 示例流程

例如，添加对新消息类型的支持：

1. 在`_extract_message_text`方法中添加对新消息类型的处理
2. 更新相关测试用例
3. 在国际化文件中添加相关翻译
4. 更新文档说明
5. 提交更改并创建PR

## 质量标准

1. 代码风格遵循 PEP 8
2. 所有公开方法和类需要有文档字符串(docstring)
3. 保持测试覆盖率在 80% 以上
4. 所有用户可见的文本使用国际化机制
5. 所有重要更改都记录在 CHANGELOG.md 中

## 有用的命令

```bash
# 运行测试
python -m unittest discover tests

# 生成测试覆盖率报告
coverage run -m unittest discover
coverage report

# 安装开发环境
pip install -e .
pip install -r requirements-dev.txt
```

## 常见问题

### 如何添加新的翻译？

1. 打开 `i18n/zh_CN.json` 和 `i18n/en_US.json`
2. 添加新的翻译键值对
3. 在代码中使用 `_()` 函数引用新的翻译键

### 如何添加支持新的语言？

1. 在 `i18n/__init__.py` 中的 `SUPPORTED_LANGUAGES` 列表中添加新语言
2. 创建相应的语言文件，例如 `i18n/ja_JP.json`
3. 翻译所有已有的字符串

## 资源链接

- [AstrBot 官方文档](https://github.com/Soulter/AstrBot/wiki)
- [Python 单元测试文档](https://docs.python.org/3/library/unittest.html)
- [原始项目仓库](https://github.com/laopanmemz/astrbot_plugin_chatsummary)