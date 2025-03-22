import os.path
from datetime import datetime
import json
from typing import List, Dict, Any, Optional
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger

@register("astrbot_plugin_chatsummary", "laopanmemz", "一个基于LLM的历史聊天记录总结插件", "1.0.3")
class ChatSummary(Star):
    """聊天记录总结插件，使用LLM进行历史消息分析和总结"""
    
    def __init__(self, context: Context):
        """初始化插件实例"""
        super().__init__(context)
        # 加载配置文件路径
        self.config_path = os.path.join('data', 'config', 'astrbot_plugin_chatsummary_config.json')
        self.admin_config_path = os.path.join('data', 'cmd_config.json')

    @filter.command("消息总结")
    async def summary(self, event: AstrMessageEvent, count: int = None, debug: str = None):
        """
        触发消息总结，命令加空格，后面跟获取聊天记录的数量即可
        
        Args:
            event: 消息事件
            count: 要获取的聊天记录数量
            debug: 调试模式标志，可选值为"debug"或"Debug"
        """
        # 类型检查和初始化
        from astrbot.core.platform.sources.aiocqhttp.aiocqhttp_message_event import AiocqhttpMessageEvent
        if not isinstance(event, AiocqhttpMessageEvent):
            yield event.plain_result("当前平台不支持消息总结功能")
            event.stop_event()
            return
            
        client = event.bot

        # 参数验证
        if count is None:
            yield event.plain_result("未传入要总结的聊天记录数量\n请按照「 /消息总结 [要总结的聊天记录数量] 」格式发送\n例如「 /消息总结 100 」")
            event.stop_event()
            return
            
        # 限制最大记录数，防止请求过大
        if count > 300:
            yield event.plain_result("请求的聊天记录数量过多，最大支持300条")
            event.stop_event()
            return

        # 获取群聊历史消息
        try:
            chat_lines = await self._fetch_group_messages(client, event.get_group_id(), count)
            
            if not chat_lines:
                yield event.plain_result("未获取到有效的聊天记录，请稍后再试")
                event.stop_event()
                return
                
            # 调试模式处理
            if debug and (debug.lower() == "debug"):
                if not self._is_admin(str(event.get_sender_id())):
                    yield event.plain_result("您无权使用调试模式")
                    return
                else:
                    prompt = self._load_prompt()
                    msg = "\n".join(chat_lines)
                    logger.info(f"prompt: {prompt}")
                    logger.info(f"chat_records: {msg}")
                    yield event.plain_result(f"prompt已通过Info Logs在控制台输出。以下为格式化后的聊天记录Debug输出：\n{msg[:1000]}...(内容过长已截断)")
                    return

            # 生成总结
            summary = await self._generate_summary(chat_lines)
            yield event.plain_result(summary)
            
        except Exception as e:
            logger.error(f"消息总结出错: {str(e)}")
            yield event.plain_result(f"消息总结失败: {str(e)}")
            event.stop_event()

    async def _fetch_group_messages(self, client, group_id: int, count: int) -> List[str]:
        """
        获取群聊历史消息并格式化
        
        Args:
            client: 机器人客户端
            group_id: 群组ID
            count: 消息数量
            
        Returns:
            格式化后的消息列表
        """
        payloads = {
            "group_id": group_id,
            "message_seq": "0",
            "count": count,
            "reverseOrder": True
        }
        
        try:
            # 调用API获取群聊历史消息
            ret = await client.api.call_action("get_group_msg_history", **payloads)
            
            # 处理消息历史记录
            messages = ret.get("messages", [])
            chat_lines = []
            
            for msg in messages:
                # 解析发送者信息
                sender = msg.get('sender', {})
                nickname = sender.get('nickname', '未知用户')
                msg_time = datetime.fromtimestamp(msg.get('time', 0))
                
                # 提取消息文本内容
                message_text = self._extract_message_text(msg.get('message', []))
                
                # 添加到聊天记录中
                if message_text:
                    chat_lines.append(f"[{msg_time}]「{nickname}」: {message_text.strip()}")
            
            return chat_lines
            
        except Exception as e:
            logger.error(f"获取群聊历史消息出错: {str(e)}")
            raise Exception(f"获取聊天记录失败: {str(e)}")

    def _extract_message_text(self, message_parts: List[Dict[str, Any]]) -> str:
        """
        从消息段中提取文本内容
        
        Args:
            message_parts: 消息段列表
            
        Returns:
            提取的文本内容
        """
        message_text = ""
        
        for part in message_parts:
            # 文本消息
            if part.get('type') == 'text':
                message_text += part.get('data', {}).get('text', '').strip() + " "
                
            # JSON消息（分享卡片等）
            elif part.get('type') == 'json':
                try:
                    json_content = json.loads(part.get('data', {}).get('data', '{}'))
                    if 'desc' in json_content.get('meta', {}).get('news', {}):
                        message_text += f"[分享内容]{json_content['meta']['news']['desc']} "
                except:
                    pass
                    
            # 表情消息
            elif part.get('type') == 'face':
                message_text += "[表情] "
                
            # 图片消息
            elif part.get('type') == 'image':
                message_text += "[图片] "
                
            # 文件消息
            elif part.get('type') == 'file':
                message_text += "[文件] "
                
            # 语音消息 
            elif part.get('type') == 'record':
                message_text += "[语音] "
                
            # @消息
            elif part.get('type') == 'at':
                at_qq = part.get('data', {}).get('qq', 'all')
                message_text += f"[@{at_qq}] "
        
        return message_text

    async def _generate_summary(self, chat_lines: List[str]) -> str:
        """
        使用LLM生成聊天记录总结
        
        Args:
            chat_lines: 格式化的聊天记录
            
        Returns:
            总结内容
        """
        msg = "\n".join(chat_lines)
        prompt = self._load_prompt()
        
        try:
            # 尝试使用AstrBot容器格式调用API（优先尝试这种方式，因为这是我们已知的工作方式）
            try:
                logger.info("尝试使用AstrBot容器格式API")
                llm_response = await self.context.get_using_provider().text_chat(
                    prompt=prompt,
                    contexts=[
                        {"role": "user", "content": msg}
                    ],
                )
                return llm_response.completion_text
            except Exception as e:
                # 如果AstrBot容器格式失败，记录错误并尝试标准OpenAI格式
                logger.info(f"AstrBot容器格式调用失败: {str(e)}，尝试使用标准OpenAI格式")
                llm_response = await self.context.get_using_provider().text_chat(
                    contexts=[
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": msg}
                    ],
                )
                return llm_response.completion_text
        except Exception as e:
            # 如果两种方式都失败，记录详细错误并抛出异常
            logger.error(f"LLM API调用失败: {str(e)}")
            raise Exception(f"生成总结失败: {str(e)}")

    def _load_prompt(self) -> str:
        """
        从配置文件加载提示词
        
        Returns:
            提示词内容
        """
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8-sig') as a:
                    config = json.load(a)
                    prompt_str = config.get('prompt', "")
                    return str(prompt_str.replace('\\n', '\n'))
            else:
                logger.warning(f"配置文件不存在: {self.config_path}")
                # 返回默认提示词
                return "- Role: 社群聊天记录总结分析师\n- Background: 你需要对群聊记录进行专业分析，提取关键信息并以美观、生动的格式呈现，帮助用户快速了解群聊精华内容。\n- Requirements:\n  1. 排版美观：使用「·」或「-」作为行前导符，适当使用空行分隔不同部分，保持层级清晰\n  2. 风格生动：避免僵硬的语气，使用生动活泼的表达方式描述群聊内容\n  3. 内容精炼：提取真正重要和有趣的内容，避免冗余\n  4. 符号使用：避免过度使用星号(*)和加粗标记，优先使用简洁的符号\n  5. 结构清晰：使用明确的分类和小标题，但不要过于机械化\n  6. 保持温度：用温暖自然的语气总结，仿佛是群里的一位细心观察者\n- OutputFormat: 按以下结构输出，但确保风格自然流畅：\n  1. 【今日速览】：简短概括群聊主要内容和氛围\n  2. 【热门话题】：按重要性排序的讨论话题，使用简洁的描述和关键要点\n  3. 【趣味时刻】：有趣的互动和金句，注重幽默和亮点\n  4. 【通知与提醒】：如果有任何重要通知或需要注意的事项\n  5. 【闲聊杂谈】：其他值得一提的小话题\n  6. 【群聊温度计】：对整体氛围的简短点评，语气轻松活泼\n- Style: 行文风格应当亲切自然，像是群里的老友在分享今日见闻，避免公式化和机械感。使用适当的表情符号增加活力，但不要过度。"
        except Exception as e:
            logger.error(f"加载提示词出错: {str(e)}")
            # 出错时返回备用提示词
            return "请对以下聊天记录进行总结，提取关键信息和讨论要点，使用生动自然的语言。"

    def _is_admin(self, user_id: str) -> bool:
        """
        检查用户是否为管理员
        
        Args:
            user_id: 用户ID
            
        Returns:
            是否为管理员
        """
        try:
            if os.path.exists(self.admin_config_path):
                with open(self.admin_config_path, 'r', encoding='utf-8-sig') as f:
                    config = json.load(f)
                    return str(user_id) in config.get('admins_id', [])
            return False
        except Exception as e:
            logger.error(f"加载管理员配置出错: {str(e)}")
            return False