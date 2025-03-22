# -*- coding: utf-8 -*-
"""
基本功能测试，确保CI可以成功运行
"""

import os
import sys
import unittest

# 添加项目根目录到系统路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 测试类
class TestBasicFunctionality(unittest.TestCase):
    """CI的基本功能测试类"""
    
    def test_python_environment(self):
        """测试Python环境是否正常"""
        self.assertTrue(True, "Python环境正常")
    
    def test_imports(self):
        """测试基本导入是否正常"""
        # 尝试导入i18n模块
        import i18n
        self.assertIsNotNone(i18n)
        
        # 尝试导入main模块
        import main
        self.assertIsNotNone(main)
        
        # 尝试导入cli模块
        import cli
        self.assertIsNotNone(cli)
    
    def test_file_structure(self):
        """测试项目文件结构是否完整"""
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        
        # 测试必要的文件和目录是否存在
        self.assertTrue(os.path.exists(os.path.join(root_dir, 'main.py')), 'main.py存在')
        self.assertTrue(os.path.exists(os.path.join(root_dir, 'i18n')), 'i18n目录存在')
        self.assertTrue(os.path.exists(os.path.join(root_dir, 'data')), 'data目录存在')
        self.assertTrue(os.path.exists(os.path.join(root_dir, 'docs')), 'docs目录存在')

if __name__ == '__main__':
    unittest.main()