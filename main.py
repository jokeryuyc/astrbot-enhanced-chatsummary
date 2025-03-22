"""
聊天记录总结插件 - 增强版
提供智能的聊天记录总结功能，支持多平台和多语言
"""

import os
import json
from datetime import datetime
import logging
from typing import List, Dict, Any, Optional

from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
import astrbot.api.message_components as Comp

# 导入国际化支持
from i18n.i18n import I18n

# 设置日志
logger = logging.getLogger("astrbot.plugin.chatsummary")

@register("astrbot_enhanced_chatsummary", "jokeryuyc", 
         "增强版聊天记录总结插件，支持多语言和更多功能", "1.0.3", 
         "https://github.com/jokeryuyc/astrbot-enhanced-chatsummary")
class EnhancedChatSummary(Star):
    """聊天记录总结插件主类，提供智能的聊天记录总结功能"""
    
    def __init__(self, context: Context, config: Dict[str, Any] = None):
        """初始化插件实例
        
        Args:
            context: AstrBot上下文
            config: 插件配置
        """
        super().__init__(context)
        self.config = config or {}
        
        # 初始化i18n
        self.i18n = I18n(default_language="zh_CN")
        
        # 获取配置项
        self.max_records = self.config.get("max_records", 300)
        self.extract_image_text = self.config.get("extract_image_text", False)
        self.debug_mode = self.config.get("debug_mode", False)
        
        logger.info(f"EnhancedChatSummary plugin initialized with max_records={self.max_records}")

    @filter.command("消息总结")
    async def summary(self, event: AstrMessageEvent, count: int = None, debug: str = None):
        """触发消息总结，命令加空格，后面跟获取聊天记录的数量
        
        Args:
            event: 消息事件
            count: 要获取的聊天记录数量
            debug: 调试参数，输入"debug"开启调试模式
        """
        # 检查参数
        if count is None:
            yield event.plain_result(self.i18n.t("missing_count_param"))
            event.stop_event()
            return
            
        # 检查记录数量是否超过最大限制
        if count > self.max_records:
            yield event.plain_result(self.i18n.t("exceeded_max_records", 
                                             count=count, 
                                             max_records=self.max_records))
            count = self.max_records
            
        # 检查debug参数
        is_debug = debug == "debug" or self.debug_mode
        if is_debug:
            # 检查是否有管理员权限
            if not await self._is_admin(event):
                yield event.plain_result(self.i18n.t("debug_permission_denied"))
                event.stop_event()
                return
                
        # 获取消息历史
        try:
            messages = await self._get_message_history(event, count)
            if not messages:
                yield event.plain_result(self.i18n.t("no_messages_found"))
                event.stop_event()
                return
                
            # 处理消息历史记录
            chat_records = await self._process_messages(event, messages)
            if not chat_records:
                yield event.plain_result(self.i18n.t("no_valid_messages"))
                event.stop_event()
                return
                
            # 如果是调试模式，输出原始记录
            if is_debug:
                yield event.plain_result(self.i18n.t("debug_raw_messages") + "\n\n" + "\n".join(chat_records))
                
            # 调用LLM生成总结
            summary = await self._generate_summary(chat_records)
            
            # 发送总结结果
            yield event.plain_result(summary)
            
        except Exception as e:
            logger.error(f"Error in summary command: {str(e)}", exc_info=True)
            yield event.plain_result(self.i18n.t("summary_error", error=str(e)))
            event.stop_event()
