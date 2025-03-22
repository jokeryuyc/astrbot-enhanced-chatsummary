#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
国际化支持模块 - i18n主要实现类
本模块提供了插件的国际化支持功能，允许在不同语言环境下使用插件
"""

import os
import json
import logging
from typing import Dict, Optional, Any

# 设置日志记录器
logger = logging.getLogger("chat_summary.i18n")

class I18nManager:
    """国际化管理器类，处理文本本地化和翻译"""
    
    def __init__(self, lang_code: str = "en_US"):
        """
        初始化I18n管理器
        
        Args:
            lang_code: 语言代码，默认为"en_US"
        """
        self.lang_code = lang_code
        self.translations: Dict[str, Dict[str, str]] = {}
        self.current_translations: Dict[str, str] = {}
        self._load_translations()
    
    def _load_translations(self) -> None:
        """加载所有可用的翻译文件"""
        try:
            # 获取当前目录路径（i18n文件夹）
            i18n_dir = os.path.dirname(os.path.abspath(__file__))
            
            # 搜索目录中的所有JSON文件
            for filename in os.listdir(i18n_dir):
                if filename.endswith(".json"):
                    lang_code = filename.replace(".json", "")
                    file_path = os.path.join(i18n_dir, filename)
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            self.translations[lang_code] = json.load(f)
                            logger.debug(f"Loaded translation: {lang_code}")
                    except Exception as e:
                        logger.error(f"Failed to load translation file {filename}: {str(e)}")
            
            # 加载当前语言的翻译
            self._set_language(self.lang_code)
        except Exception as e:
            logger.error(f"Error loading translations: {str(e)}")
            # 确保至少有一个空字典防止后续操作失败
            self.current_translations = {}
    
    def _set_language(self, lang_code: str) -> None:
        """
        设置当前使用的语言
        
        Args:
            lang_code: 语言代码
        """
        if lang_code in self.translations:
            self.lang_code = lang_code
            self.current_translations = self.translations[lang_code]
            logger.info(f"Language set to: {lang_code}")
        else:
            # 如果请求的语言不可用，回退到英语
            fallback = "en_US"
            if fallback in self.translations:
                self.lang_code = fallback
                self.current_translations = self.translations[fallback]
                logger.warning(f"Requested language {lang_code} not available, falling back to {fallback}")
            else:
                # 如果连英语也不可用，使用任何可用的语言
                if self.translations:
                    first_available = next(iter(self.translations.keys()))
                    self.lang_code = first_available
                    self.current_translations = self.translations[first_available]
                    logger.warning(f"Falling back to available language: {first_available}")
                else:
                    # 如果没有任何翻译可用
                    self.current_translations = {}
                    logger.error("No translations available")
    
    def get_text(self, key: str, default: Optional[str] = None) -> str:
        """
        获取指定键的本地化文本
        
        Args:
            key: 翻译键
            default: 如果翻译不存在时的默认值
            
        Returns:
            本地化的文本字符串
        """
        if key in self.current_translations:
            return self.current_translations[key]
        
        # 在其他可用语言中查找
        for lang, translations in self.translations.items():
            if lang != self.lang_code and key in translations:
                text = translations[key]
                logger.debug(f"Key '{key}' not found in {self.lang_code}, using value from {lang}")
                return text
        
        # 如果所有语言都没有这个键，返回默认值或键本身
        if default is not None:
            return default
        return key
    
    def change_language(self, lang_code: str) -> bool:
        """
        更改当前使用的语言
        
        Args:
            lang_code: 新的语言代码
            
        Returns:
            是否成功切换语言
        """
        if lang_code in self.translations:
            self._set_language(lang_code)
            return True
        return False
    
    def get_available_languages(self) -> Dict[str, Any]:
        """
        获取所有可用语言及其元数据
        
        Returns:
            语言代码及其元数据的字典
        """
        result = {}
        for lang_code in self.translations.keys():
            # 尝试获取语言的元数据（如果存在）
            meta = {}
            if lang_code in self.translations and "_meta" in self.translations[lang_code]:
                meta = self.translations[lang_code]["_meta"]
            
            result[lang_code] = {
                "name": meta.get("name", lang_code),
                "native_name": meta.get("native_name", lang_code),
                "is_current": lang_code == self.lang_code
            }
        return result


# 单例模式
_i18n_instance = None

def get_i18n_manager(lang_code: Optional[str] = None) -> I18nManager:
    """
    获取I18n管理器实例（单例模式）
    
    Args:
        lang_code: 可选的语言代码，用于初始化或切换语言
        
    Returns:
        I18nManager实例
    """
    global _i18n_instance
    if _i18n_instance is None:
        _i18n_instance = I18nManager(lang_code or "en_US")
    elif lang_code and _i18n_instance.lang_code != lang_code:
        _i18n_instance.change_language(lang_code)
    return _i18n_instance

def _(key: str, default: Optional[str] = None) -> str:
    """
    获取翻译的便捷函数
    
    Args:
        key: 翻译键
        default: 默认值
        
    Returns:
        翻译后的文本
    """
    return get_i18n_manager().get_text(key, default)