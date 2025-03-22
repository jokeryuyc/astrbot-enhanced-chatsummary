# 此文件被移动到 _test_chatsummary.py
# 只在本地环境中使用，CI环境中跳过

import pytest

@pytest.mark.skip(reason="仅保留为占位符，避免导入错误")
def test_dummy():
    """占位测试，永远被跳过，防止导入错误"""
    pass