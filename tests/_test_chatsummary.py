# 此文件是原始 test_chatsummary.py 的备份副本
# 通过修改文件名，确保 pytest 不会自动收集它
# 该测试文件依赖于 AstrBot 环境，只在非 CI 环境中运行

import unittest
from unittest.mock import AsyncMock, MagicMock, patch
import sys
import os
import json
import pytest

# 添加项目根目录到系统路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 导入要测试的模块
from main import ChatSummary

# 使用pytest.mark.skip装饰器来标记这个测试类
@pytest.mark.skip(reason="Skip AstrBot specific tests in CI environment")
class TestChatSummary(unittest.TestCase):
    """聊天总结插件的单元测试类"""
    
    def setUp(self):
        """测试前准备"""
        # 模拟 Context 对象
        self.mock_context = MagicMock()
        # 创建插件实例
        self.chat_summary = ChatSummary(self.mock_context)
        # 模拟配置文件路径
        self.chat_summary.config_path = os.path.join('tests', 'test_data', 'config.json')
        self.chat_summary.admin_config_path = os.path.join('tests', 'test_data', 'admin_config.json')
        
        # 创建测试数据目录
        os.makedirs(os.path.join('tests', 'test_data'), exist_ok=True)
        
        # 创建测试配置文件
        with open(self.chat_summary.config_path, 'w', encoding='utf-8') as f:
            json.dump({
                'prompt': 'Test prompt',
                'max_records': 100,
                'extract_image_text': False,
                'debug_mode': {'enabled': False, 'log_level': 'info'}
            }, f)
            
        # 创建测试管理员配置文件
        with open(self.chat_summary.admin_config_path, 'w', encoding='utf-8') as f:
            json.dump({
                'admins_id': ['123456']
            }, f)
    
    def tearDown(self):
        """测试后清理"""
        # 删除测试配置文件
        if os.path.exists(self.chat_summary.config_path):
            os.remove(self.chat_summary.config_path)
        if os.path.exists(self.chat_summary.admin_config_path):
            os.remove(self.chat_summary.admin_config_path)
            
        # 如果目录为空，删除测试目录
        if not os.listdir(os.path.join('tests', 'test_data')):
            os.rmdir(os.path.join('tests', 'test_data'))
    
    def test_load_prompt(self):
        """测试加载提示词功能"""
        # 调用测试方法
        prompt = self.chat_summary._load_prompt()
        
        # 验证结果
        self.assertEqual(prompt, 'Test prompt', "提示词加载错误")
    
    def test_is_admin(self):
        """测试管理员验证功能"""
        # 测试管理员账号
        is_admin = self.chat_summary._is_admin('123456')
        self.assertTrue(is_admin, "管理员验证失败")
        
        # 测试非管理员账号
        is_admin = self.chat_summary._is_admin('654321')
        self.assertFalse(is_admin, "非管理员验证失败")
    
    @patch('main.logger')
    def test_extract_message_text(self, mock_logger):
        """测试消息文本提取功能"""
        # 测试文本消息
        text_message = [{'type': 'text', 'data': {'text': 'Hello world'}}]
        result = self.chat_summary._extract_message_text(text_message)
        self.assertEqual(result, 'Hello world ', "文本消息提取失败")
        
        # 测试表情消息
        face_message = [{'type': 'face', 'data': {'id': '21'}}]
        result = self.chat_summary._extract_message_text(face_message)
        self.assertEqual(result, '[表情] ', "表情消息提取失败")
        
        # 测试图片消息
        image_message = [{'type': 'image', 'data': {'file': 'test.jpg'}}]
        result = self.chat_summary._extract_message_text(image_message)
        self.assertEqual(result, '[图片] ', "图片消息提取失败")
        
        # 测试混合消息
        mixed_message = [
            {'type': 'text', 'data': {'text': 'Hello'}},
            {'type': 'face', 'data': {'id': '21'}},
            {'type': 'image', 'data': {'file': 'test.jpg'}}
        ]
        result = self.chat_summary._extract_message_text(mixed_message)
        self.assertEqual(result, 'Hello [表情] [图片] ', "混合消息提取失败")


# 新增一个非AstrBot依赖的测试类，可以在CI中运行
class TestBasicFunctionality(unittest.TestCase):
    """基本功能测试类，无需AstrBot环境"""
    
    def setUp(self):
        # 模拟上下文和配置
        self.mock_context = MagicMock()
        self.config = {
            "language": "en_US",
            "max_records": 100,
            "debug_mode": {"enabled": False}
        }
        # 创建插件实例
        from main import EnhancedChatSummary
        self.chat_summary = EnhancedChatSummary(self.mock_context, self.config)
    
    def test_initialization(self):
        """测试初始化"""
        self.assertEqual(self.chat_summary.max_records, 100)
        self.assertFalse(self.chat_summary.debug_mode)
        self.assertEqual(self.chat_summary.i18n.lang, "en_US")
    
    def test_extract_message_text(self):
        """测试消息文本提取功能"""
        # 测试文本消息
        text_message = [{'type': 'text', 'data': {'text': 'Test message'}}]
        result = self.chat_summary._extract_message_text(text_message)
        self.assertEqual(result, 'Test message ', "文本消息提取失败")

if __name__ == '__main__':
    unittest.main()