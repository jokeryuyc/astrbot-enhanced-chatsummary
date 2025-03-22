import unittest
from unittest.mock import AsyncMock, MagicMock, patch
import sys
import os
import json

# 添加项目根目录到系统路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 导入要测试的模块
from main import ChatSummary

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
    
    @patch('main.logger')
    async def test_generate_summary(self, mock_logger):
        """测试生成总结功能"""
        # 准备测试数据
        chat_lines = [
            "[2022-01-01 12:00:00]「用户A」: 大家好",
            "[2022-01-01 12:01:00]「用户B」: 你好啊",
            "[2022-01-01 12:02:00]「用户C」: 今天天气真好"
        ]
        
        # 模拟LLM返回结果
        mock_llm_response = MagicMock()
        mock_llm_response.completion_text = "今日聊天总结"
        
        # 模拟API调用
        mock_provider = MagicMock()
        mock_provider.text_chat = AsyncMock(return_value=mock_llm_response)
        self.mock_context.get_using_provider.return_value = mock_provider
        
        # 调用测试方法
        result = await self.chat_summary._generate_summary(chat_lines)
        
        # 验证结果
        self.assertEqual(result, "今日聊天总结", "生成总结失败")
        # 验证API调用
        mock_provider.text_chat.assert_called_once()
    
    @patch('main.logger')
    async def test_summary_command(self, mock_logger):
        """测试总结命令功能"""
        # 模拟事件对象
        mock_event = MagicMock()
        mock_event.get_group_id.return_value = 123456
        mock_event.get_sender_id.return_value = '123456'  # 管理员ID
        mock_event.plain_result = MagicMock()
        mock_event.stop_event = MagicMock()
        
        # 模拟客户端对象
        mock_client = MagicMock()
        mock_event.bot = mock_client
        
        # 模拟消息历史记录
        mock_messages = {
            "messages": [
                {
                    "sender": {"nickname": "用户A"},
                    "time": 1640995200,  # 2022-01-01 12:00:00
                    "message": [{"type": "text", "data": {"text": "大家好"}}]
                }
            ]
        }
        
        # 模拟调用结果
        mock_client.api.call_action = AsyncMock(return_value=mock_messages)
        
        # 模拟LLM生成总结
        self.chat_summary._generate_summary = AsyncMock(return_value="测试总结结果")
        
        # 测试正常情况
        gen = self.chat_summary.summary(mock_event, 10)
        result = [r async for r in gen]  # 获取异步执行结果
        
        # 验证结果
        self.assertEqual(len(result), 1, "命令执行应返回一个结果")
        mock_event.plain_result.assert_called_once_with("测试总结结果")
        
        # 测试缺少参数情况
        mock_event.reset_mock()
        gen = self.chat_summary.summary(mock_event)
        result = [r async for r in gen]  # 获取异步执行结果
        
        # 验证结果
        self.assertEqual(len(result), 1, "命令执行应返回一个结果")
        mock_event.plain_result.assert_called_once()
        mock_event.stop_event.assert_called_once()

if __name__ == '__main__':
    unittest.main()