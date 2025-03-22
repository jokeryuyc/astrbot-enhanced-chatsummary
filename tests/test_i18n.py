#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试i18n国际化模块的功能
"""

import os
import json
import unittest
from unittest.mock import patch, mock_open
import sys
import tempfile

# 添加项目根目录到系统路径，确保可以导入模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from i18n.i18n import I18nManager, get_i18n_manager, _


class TestI18n(unittest.TestCase):
    """测试I18n模块的功能"""

    def setUp(self):
        """每个测试前的准备工作"""
        # 创建测试用的翻译文件内容
        self.en_us_data = {
            "_meta": {
                "name": "English (US)",
                "native_name": "English (US)"
            },
            "hello": "Hello",
            "welcome": "Welcome to the application",
            "goodbye": "Goodbye"
        }
        
        self.zh_cn_data = {
            "_meta": {
                "name": "Chinese (Simplified)",
                "native_name": "中文（简体）"
            },
            "hello": "你好",
            "welcome": "欢迎使用本应用",
            "goodbye": "再见"
        }
        
        # 使用临时目录来存放测试翻译文件
        self.temp_dir = tempfile.TemporaryDirectory()
        
        # 写入测试翻译文件
        with open(os.path.join(self.temp_dir.name, "en_US.json"), "w", encoding="utf-8") as f:
            json.dump(self.en_us_data, f, ensure_ascii=False)
        
        with open(os.path.join(self.temp_dir.name, "zh_CN.json"), "w", encoding="utf-8") as f:
            json.dump(self.zh_cn_data, f, ensure_ascii=False)
    
    def tearDown(self):
        """每个测试后的清理工作"""
        # 清理临时目录
        self.temp_dir.cleanup()
        # 重置单例实例
        global _i18n_instance
        from i18n.i18n import _i18n_instance
        _i18n_instance = None
    
    @patch('os.path.dirname')
    @patch('os.listdir')
    def test_load_translations(self, mock_listdir, mock_dirname):
        """测试加载翻译文件"""
        # 模拟目录和文件列表
        mock_dirname.return_value = self.temp_dir.name
        mock_listdir.return_value = ["en_US.json", "zh_CN.json"]
        
        # 使用真实的open函数，但路径指向我们的临时目录
        manager = I18nManager()
        
        # 验证翻译是否正确加载
        self.assertEqual(len(manager.translations), 2)
        self.assertIn("en_US", manager.translations)
        self.assertIn("zh_CN", manager.translations)
        
        # 验证默认语言是否正确设置
        self.assertEqual(manager.lang_code, "en_US")
        self.assertEqual(manager.get_text("hello"), "Hello")
    
    def test_change_language(self):
        """测试更改语言功能"""
        with patch('os.path.dirname') as mock_dirname, \
             patch('os.listdir') as mock_listdir:
            
            mock_dirname.return_value = self.temp_dir.name
            mock_listdir.return_value = ["en_US.json", "zh_CN.json"]
            
            manager = I18nManager("en_US")
            
            # 验证初始语言
            self.assertEqual(manager.get_text("hello"), "Hello")
            
            # 切换到中文
            success = manager.change_language("zh_CN")
            self.assertTrue(success)
            self.assertEqual(manager.lang_code, "zh_CN")
            self.assertEqual(manager.get_text("hello"), "你好")
            
            # 尝试切换到不存在的语言
            success = manager.change_language("fr_FR")
            self.assertFalse(success)
            # 语言应该保持不变
            self.assertEqual(manager.lang_code, "zh_CN")
    
    def test_get_text_with_fallback(self):
        """测试文本获取以及默认值功能"""
        with patch('os.path.dirname') as mock_dirname, \
             patch('os.listdir') as mock_listdir:
            
            mock_dirname.return_value = self.temp_dir.name
            mock_listdir.return_value = ["en_US.json", "zh_CN.json"]
            
            manager = I18nManager("en_US")
            
            # 测试存在的翻译键
            self.assertEqual(manager.get_text("hello"), "Hello")
            
            # 测试不存在的翻译键，不设置默认值
            self.assertEqual(manager.get_text("not_exist"), "not_exist")
            
            # 测试不存在的翻译键，设置默认值
            self.assertEqual(manager.get_text("not_exist", "Default"), "Default")
    
    def test_get_available_languages(self):
        """测试获取可用语言列表"""
        with patch('os.path.dirname') as mock_dirname, \
             patch('os.listdir') as mock_listdir:
            
            mock_dirname.return_value = self.temp_dir.name
            mock_listdir.return_value = ["en_US.json", "zh_CN.json"]
            
            manager = I18nManager("en_US")
            languages = manager.get_available_languages()
            
            self.assertEqual(len(languages), 2)
            self.assertIn("en_US", languages)
            self.assertIn("zh_CN", languages)
            
            # 验证语言元数据
            self.assertEqual(languages["en_US"]["name"], "English (US)")
            self.assertEqual(languages["zh_CN"]["native_name"], "中文（简体）")
            
            # 验证当前语言标志
            self.assertTrue(languages["en_US"]["is_current"])
            self.assertFalse(languages["zh_CN"]["is_current"])
    
    def test_singleton_pattern(self):
        """测试单例模式"""
        with patch('os.path.dirname') as mock_dirname, \
             patch('os.listdir') as mock_listdir:
            
            mock_dirname.return_value = self.temp_dir.name
            mock_listdir.return_value = ["en_US.json", "zh_CN.json"]
            
            # 获取第一个实例
            manager1 = get_i18n_manager("en_US")
            self.assertEqual(manager1.lang_code, "en_US")
            
            # 获取第二个实例，应该是同一个对象
            manager2 = get_i18n_manager()
            self.assertIs(manager1, manager2)
            
            # 改变语言并获取第三个实例
            manager3 = get_i18n_manager("zh_CN")
            self.assertIs(manager1, manager3)
            self.assertEqual(manager3.lang_code, "zh_CN")
    
    def test_shortcut_function(self):
        """测试快捷函数"""
        with patch('os.path.dirname') as mock_dirname, \
             patch('os.listdir') as mock_listdir:
            
            mock_dirname.return_value = self.temp_dir.name
            mock_listdir.return_value = ["en_US.json", "zh_CN.json"]
            
            # 初始化管理器
            get_i18n_manager("en_US")
            
            # 测试快捷函数
            self.assertEqual(_("hello"), "Hello")
            self.assertEqual(_("not_exist", "Default"), "Default")
            
            # 改变语言后再测试
            get_i18n_manager("zh_CN")
            self.assertEqual(_("hello"), "你好")


if __name__ == "__main__":
    unittest.main()