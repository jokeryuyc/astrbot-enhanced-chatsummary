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

# 简化测试，导入i18n模块中的I18n类
from i18n import I18n

class TestI18n(unittest.TestCase):
    """测试I18n模块的基本功能"""

    def setUp(self):
        """每个测试前的准备工作"""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.i18n = I18n("en_US")
        
        # 模拟翻译数据
        self.i18n.translations = {
            "en_US": {
                "_meta": {
                    "name": "English (US)",
                    "native_name": "English (US)"
                },
                "hello": "Hello",
                "welcome": "Welcome to the application"
            },
            "zh_CN": {
                "_meta": {
                    "name": "Chinese (Simplified)",
                    "native_name": "中文（简体）"
                },
                "hello": "你好",
                "welcome": "欢迎使用本应用"
            }
        }
        self.i18n.lang_code = "en_US"
        self.i18n.current_translations = self.i18n.translations["en_US"]
    
    def tearDown(self):
        """每个测试后的清理工作"""
        self.temp_dir.cleanup()
    
    def test_get_text(self):
        """测试获取文本功能"""
        # 测试存在的翻译键
        self.assertEqual(self.i18n.get("hello"), "Hello")
        
        # 测试不存在的翻译键，不设置默认值
        self.assertEqual(self.i18n.get("not_exist"), "not_exist")
        
        # 测试不存在的翻译键，设置默认值
        self.assertEqual(self.i18n.get("not_exist", "Default"), "Default")
    
    def test_change_language(self):
        """测试改变语言功能"""
        # 测试初始语言
        self.assertEqual(self.i18n.get("hello"), "Hello")
        
        # 切换到中文
        self.i18n.change_language("zh_CN")
        self.assertEqual(self.i18n.lang, "zh_CN")
        self.assertEqual(self.i18n.get("hello"), "你好")
        
        # 尝试切换到不存在的语言
        result = self.i18n.change_language("fr_FR")
        self.assertFalse(result)
        # 语言应该保持不变
        self.assertEqual(self.i18n.lang, "zh_CN")

if __name__ == "__main__":
    unittest.main()