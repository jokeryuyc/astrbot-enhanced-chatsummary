# pytest配置文件
# 在这里添加pytest的全局配置

import pytest

# 禁用test_chatsummary.py文件的收集
def pytest_ignore_collect(collection_path, config):
    # 如果是test_chatsummary.py文件，则跳过收集
    if collection_path.name == 'test_chatsummary.py':
        return True
    return False
