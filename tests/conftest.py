# -*- coding: utf-8 -*-
"""
测试配置文件，提供测试矩阵和公共模拟对象
"""

import os
import sys
import pytest

# 添加项目根目录到系统路径
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, _ROOT)

# 创建测试数据目录
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'test_data')
os.makedirs(TEST_DATA_DIR, exist_ok=True)

# 确保测试环境标记
os.environ['TESTING'] = 'True'

@pytest.fixture
def sample_config():
    """提供示例配置数据用于测试"""
    return {
        "language": "en_US",
        "summary_format": "markdown",
        "summary_length": "medium",
        "include_timestamps": True,
        "include_participants": True,
        "highlight_keywords": True,
        "max_message_count": 100,
        "debug_mode": {
            "enabled": False,
            "log_level": "info"
        }
    }

@pytest.fixture
def mock_context():
    """提供模拟的Context对象"""
    class MockContext:
        def __init__(self):
            pass
            
        def get_using_provider(self):
            return MockProvider()
    
    return MockContext()

@pytest.fixture
def mock_provider():
    """提供模拟的Provider对象"""
    class MockProvider:
        async def text_chat(self, input, max_tokens=None, temperature=None):
            class MockResponse:
                completion_text = "模拟的总结结果 - 测试环境"
            return MockResponse()
    
    return MockProvider()