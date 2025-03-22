# 测试说明

本目录包含 AstrBot 增强版聊天总结插件的测试用例。

## 测试结构

- `test_chatsummary.py`: 测试插件的核心功能
- `test_data/`: 存放测试数据的目录

## 运行测试

从项目根目录运行测试：

```bash
python -m unittest discover tests
```

运行单个测试文件：

```bash
python -m unittest tests.test_chatsummary
```

运行特定测试方法：

```bash
python -m unittest tests.test_chatsummary.TestChatSummary.test_load_prompt
```

## 测试覆盖率

要生成测试覆盖率报告，请安装并运行 coverage：

```bash
pip install coverage
coverage run -m unittest discover
coverage report
```

生成HTML格式的详细报告：

```bash
coverage html
```

报告将生成在`htmlcov/`目录中。