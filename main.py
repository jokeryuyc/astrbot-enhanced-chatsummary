"""
聊天记录总结插件 - 增强版
提供智能的聊天记录总结功能，支持多平台和多语言
"""

import os
import json
from datetime import datetime
import logging
from typing import List, Dict, Any, Optional, Union, Type
import time

# 定义模拟类型，使它们在不导入AstrBot的情况下也能使用
class MockContext:
    """模拟的Context类，用于测试环境"""
    def get_using_provider(self):
        return MockProvider()

class MockProvider:
    """模拟的Provider类，用于测试环境"""
    async def text_chat(self, input, max_tokens=None, temperature=None):
        class MockResponse:
            completion_text = "模拟的总结结果 - 测试环境"
        return MockResponse()

class MockStar:
    """模拟的Star类，用于测试环境"""
    def __init__(self, context=None):
        self.context = context or MockContext()

# 尝试导入AstrBot依赖，如果未安装则使用Mock对象进行测试
try:
    from astrbot.api.event import filter, AstrMessageEvent
    from astrbot.api.star import Context, Star, register
    import astrbot.api.message_components as Comp
    ASTRBOT_AVAILABLE = True
except ImportError:
    ASTRBOT_AVAILABLE = False
    # 定义模拟的函数和类
    Context = MockContext
    Star = MockStar
    filter = type('MockFilter', (), {'command': lambda x: lambda y: y})
    register = lambda *args, **kwargs: lambda cls: cls

# 导入国际化支持
from i18n import I18n

# 设置日志
logger = logging.getLogger("astrbot.plugin.chatsummary")

# 插件类定义
@register("astrbot_enhanced_chatsummary", "jokeryuyc", 
         "增强版聊天记录总结插件，支持多语言和更多功能", "1.0.3", 
         "https://github.com/jokeryuyc/astrbot-enhanced-chatsummary")
class EnhancedChatSummary(MockStar if not ASTRBOT_AVAILABLE else Star):
    """聊天记录总结插件主类，提供智能的聊天记录总结功能"""
    
    def __init__(self, context: Any, config: Dict[str, Any] = None):
        """初始化插件实例
        
        Args:
            context: AstrBot上下文
            config: 插件配置
        """
        if ASTRBOT_AVAILABLE:
            super().__init__(context)
        else:
            super().__init__(context)
        
        self.context = context
        self.config = config or {}
        
        # 初始化i18n
        self.i18n = I18n(self.config.get("language", "zh_CN"))
        
        # 获取配置项
        self.max_records = self.config.get("max_records", 300)
        self.extract_image_text = self.config.get("extract_image_text", False)
        self.debug_mode = self.config.get("debug_mode", {}).get("enabled", False)
        
        # 配置文件路径
        self.config_path = os.path.join('data', 'config', 'config.json')
        self.admin_config_path = os.path.join('data', 'config', 'admin_config.json')
        
        logger.info(f"EnhancedChatSummary plugin initialized with max_records={self.max_records}")

    def _load_prompt(self) -> str:
        """从配置文件中加载提示词
        
        Returns:
            加载的提示词
        """
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    return config.get('prompt', 'Default prompt')
            return 'Default prompt'
        except Exception as e:
            logger.error(f"Error loading prompt: {e}")
            return 'Default prompt'
    
    def _is_admin(self, user_id: str) -> bool:
        """检查用户是否是管理员
        
        Args:
            user_id: 用户ID
            
        Returns:
            是否为管理员
        """
        try:
            if os.path.exists(self.admin_config_path):
                with open(self.admin_config_path, 'r', encoding='utf-8') as f:
                    admin_config = json.load(f)
                    return user_id in admin_config.get('admins_id', [])
            return False
        except Exception as e:
            logger.error(f"Error checking admin status: {e}")
            return False
            
    async def _is_admin(self, event) -> bool:
        """异步检查用户是否是管理员
        
        Args:
            event: 消息事件
            
        Returns:
            是否为管理员
        """
        try:
            user_id = event.get_sender_id()
            return self._is_admin(user_id)
        except:
            return False  # 在测试环境中返回false

    def _extract_message_text(self, message_segments: List[Dict[str, Any]]) -> str:
        """提取消息文本
        
        Args:
            message_segments: 消息段列表
            
        Returns:
            提取的文本内容
        """
        result = ""
        try:
            for segment in message_segments:
                msg_type = segment.get('type', '')
                data = segment.get('data', {})
                
                if msg_type == 'text':
                    result += data.get('text', '') + ' '
                elif msg_type == 'face':
                    result += '[表情] '
                elif msg_type == 'image':
                    # 如果开启了图片文本提取功能，未来可以调用OCR服务
                    result += '[图片] '
                else:
                    result += f'[{msg_type}] '
        except Exception as e:
            logger.error(f"Error extracting message text: {e}")
            
        return result
    
    async def _get_message_history(self, event, count: int) -> List[Dict[str, Any]]:
        """获取消息历史
        
        Args:
            event: 消息事件
            count: 要获取的消息数量
            
        Returns:
            消息历史列表
        """
        try:
            if not ASTRBOT_AVAILABLE:
                # 在测试环境中返回模拟数据
                return [
                    {
                        'sender': {'nickname': '测试用户A'},
                        'time': int(time.time()),
                        'message': [{'type': 'text', 'data': {'text': '你好，这是测试消息'}}]
                    },
                    {
                        'sender': {'nickname': '测试用户B'},
                        'time': int(time.time()) - 60,
                        'message': [{'type': 'text', 'data': {'text': '这是一条回复消息'}}]
                    }
                ]
                
            # 实际环境中的代码
            group_id = event.get_group_id()
            messages = await event.bot.api.call_action(
                'get_group_msg_history',
                group_id=group_id,
                count=count
            )
            return messages.get('messages', [])
        except Exception as e:
            logger.error(f"Error getting message history: {e}")
            return []
    
    async def _process_messages(self, event, messages: List[Dict[str, Any]]) -> List[str]:
        """处理消息历史记录
        
        Args:
            event: 消息事件
            messages: 消息历史列表
            
        Returns:
            处理后的聊天记录列表
        """
        chat_records = []
        try:
            for msg in messages:
                # 获取发送者昵称
                sender = msg.get('sender', {}).get('nickname', 'Unknown')
                # 获取消息时间
                msg_time = msg.get('time', 0)
                time_str = datetime.fromtimestamp(msg_time).strftime('%Y-%m-%d %H:%M:%S')
                # 获取消息内容
                message = msg.get('message', [])
                text = self._extract_message_text(message)
                
                # 格式化聊天记录
                chat_records.append(f"[{time_str}]「{sender}」: {text}")
                
            # 反转消息顺序（从旧到新）
            chat_records.reverse()
            return chat_records
        except Exception as e:
            logger.error(f"Error processing messages: {e}")
            return []
    
    async def _generate_summary(self, chat_lines: List[str]) -> str:
        """生成聊天总结
        
        Args:
            chat_lines: 聊天记录行
            
        Returns:
            生成的总结文本
        """
        try:
            # 加载提示词
            prompt = self._load_prompt()
            
            # 构建输入文本
            input_text = f"{prompt}\n\n{''.join(chat_lines)}"
            
            # 如果没有AstrBot环境，返回模拟响应
            if not ASTRBOT_AVAILABLE:
                return "模拟的总结结果 - 测试环境"  # 用于测试
            
            # 获取LLM提供商
            provider = self.context.get_using_provider()
            
            # 调用LLM生成总结
            response = await provider.text_chat(
                input=input_text,
                max_tokens=1024,
                temperature=0.7
            )
            
            # 返回生成的总结
            return response.completion_text
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return f"生成总结时出错: {str(e)}"

    @filter.command("消息总结")
    async def summary(self, event, count: Optional[int] = None, debug: Optional[str] = None):
        """触发消息总结，命令加空格，后面跟获取聊天记录的数量
        
        Args:
            event: 消息事件
            count: 要获取的聊天记录数量
            debug: 调试参数，输入"debug"开启调试模式
        """
        # 检查参数
        if count is None:
            if hasattr(event, 'plain_result'):
                yield event.plain_result("请提供要获取的消息数量，例如：消息总结 100")
            if hasattr(event, 'stop_event'):
                event.stop_event()
            return
            
        # 检查记录数量是否超过最大限制
        if count > self.max_records:
            if hasattr(event, 'plain_result'):
                yield event.plain_result(f"请求的消息数量 {count} 超过了最大限制 {self.max_records}")
            count = self.max_records
            
        # 检查debug参数
        is_debug = debug == "debug" or self.debug_mode
        if is_debug:
            # 检查是否有管理员权限
            if not await self._is_admin(event):
                if hasattr(event, 'plain_result'):
                    yield event.plain_result("只有管理员可以使用调试模式")
                if hasattr(event, 'stop_event'):
                    event.stop_event()
                return
                
        # 获取消息历史
        try:
            messages = await self._get_message_history(event, count)
            if not messages:
                if hasattr(event, 'plain_result'):
                    yield event.plain_result("未找到消息历史记录")
                if hasattr(event, 'stop_event'):
                    event.stop_event()
                return
                
            # 处理消息历史记录
            chat_records = await self._process_messages(event, messages)
            if not chat_records:
                if hasattr(event, 'plain_result'):
                    yield event.plain_result("未找到有效的消息记录")
                if hasattr(event, 'stop_event'):
                    event.stop_event()
                return
                
            # 如果是调试模式，输出原始记录
            if is_debug:
                if hasattr(event, 'plain_result'):
                    yield event.plain_result("调试模式：原始消息记录" + "\n\n" + "\n".join(chat_records))
                
            # 调用LLM生成总结
            summary = await self._generate_summary(chat_records)
            
            # 发送总结结果
            if hasattr(event, 'plain_result'):
                yield event.plain_result(summary)
            else:
                yield summary
            
        except Exception as e:
            logger.error(f"Error in summary command: {str(e)}", exc_info=True)
            if hasattr(event, 'plain_result'):
                yield event.plain_result(f"生成总结时出错: {str(e)}")
            if hasattr(event, 'stop_event'):
                event.stop_event()

# 为了兼容测试，提供ChatSummary别名
ChatSummary = EnhancedChatSummary
