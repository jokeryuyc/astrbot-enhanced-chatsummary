"""国际化支持包"""

import os
import json
from typing import Dict, Optional

# 支持的语言
SUPPORTED_LANGUAGES = ['zh_CN', 'en_US']

# 默认语言
DEFAULT_LANGUAGE = 'zh_CN'

class I18n:
    """国际化类，用于处理多语言翻译"""
    
    def __init__(self, lang: str = DEFAULT_LANGUAGE):
        """初始化国际化实例
        
        Args:
            lang: 语言代码，例如 'zh_CN', 'en_US'
        """
        self.lang = lang if lang in SUPPORTED_LANGUAGES else DEFAULT_LANGUAGE
        self.translations: Dict[str, Dict[str, str]] = {}
        self._load_translations()
    
    def _load_translations(self) -> None:
        """加载翻译文件"""
        for lang in SUPPORTED_LANGUAGES:
            try:
                # 获取当前脚本所在目录
                current_dir = os.path.dirname(os.path.abspath(__file__))
                # 拼接翻译文件路径
                file_path = os.path.join(current_dir, f"{lang}.json")
                
                # 加载翻译文件
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.translations[lang] = json.load(f)
            except Exception as e:
                print(f"Error loading translation for {lang}: {e}")
                # 如果加载失败，初始化为空字典
                self.translations[lang] = {}
    
    def get(self, key: str, **kwargs) -> str:
        """获取指定键的翻译
        
        Args:
            key: 翻译键
            **kwargs: 用于格式化的参数
            
        Returns:
            翻译后的文本。如果找不到翻译，返回键本身
        """
        # 获取当前语言的翻译
        translation = self.translations.get(self.lang, {})
        # 获取翻译文本，如果不存在，则尝试使用默认语言
        text = translation.get(key)
        
        if text is None and self.lang != DEFAULT_LANGUAGE:
            # 如果当前语言不是默认语言，尝试使用默认语言
            default_translation = self.translations.get(DEFAULT_LANGUAGE, {})
            text = default_translation.get(key, key)
        else:
            # 如果在当前语言中找不到，或者当前语言就是默认语言，则使用键本身
            text = text or key
        
        # 如果有格式化参数，进行格式化
        if kwargs and isinstance(text, str):
            try:
                return text.format(**kwargs)
            except KeyError:
                # 如果格式化失败，返回原始文本
                return text
        
        return text
    
    def change_language(self, lang: str) -> bool:
        """更改当前语言
        
        Args:
            lang: 新的语言代码
            
        Returns:
            是否成功更改语言
        """
        if lang in SUPPORTED_LANGUAGES:
            self.lang = lang
            return True
        return False

# 创建默认实例
_i18n = I18n()

def get(key: str, **kwargs) -> str:
    """获取翻译的全局方法"""
    return _i18n.get(key, **kwargs)

def change_language(lang: str) -> bool:
    """更改当前语言的全局方法"""
    return _i18n.change_language(lang)