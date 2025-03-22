# AstrBot 聊天记录智能总结插件

![AstrBot](https://img.shields.io/badge/AstrBot-Plugin-blue)
![License](https://img.shields.io/badge/license-AGPL--3.0-green)
![Python](https://img.shields.io/badge/python-3.8%2B-yellow)
![Version](https://img.shields.io/badge/version-1.0.2-orange)

一个专业的基于 AstrBot 框架的插件，利用大型语言模型(LLM)技术，通过智能分析群聊历史记录，生成高质量的结构化摘要。本插件旨在帮助群组管理员和成员快速了解群内重要信息和讨论内容，提高信息获取效率。

<p align="center">
  <img src="https://raw.githubusercontent.com/jokeryuyc/astrbot-enhanced-chatsummary/main/docs/images/demo.png" alt="Demo" width="600">
</p>

## 🌟 核心特性

- **智能内容提取**: 自动识别并提取群聊中的关键信息，减少信息噪音
- **结构化输出**: 将混乱的群聊内容转化为清晰的结构化摘要，便于快速浏览
- **热点分级**: 基于讨论热度对话题进行智能分级(☆-☆☆☆☆☆)，突出重点内容
- **隐私保护**: 在总结过程中尊重用户隐私，适当处理敏感信息
- **高度可定制**: 支持自定义提示词和多种配置参数，满足不同场景需求
- **开发者友好**: 内置调试模式，便于插件开发者测试和优化

## 📊 功能演示

**输入命令**:
```
/消息总结 100
```

**输出效果**:
```
·重要通知提醒
  - 周五下午3点项目组会议
  - 本周六团建活动地点已更改为森林公园

·讨论话题
  - 话题1：新版API文档审核
    - 内容摘要：讨论了文档格式标准；确认了审核流程；分配了审核任务
    - 讨论时间：10:15 - 10:38
  - 话题2：前端组件库更新计划
    - 内容摘要：评估了当前组件库不足；提出了迁移方案；讨论了兼容性问题
    - 讨论时间：11:05 - 11:42

·趣味互动片段
  -「用户A」：分享了一个程序员笑话，引发群内热烈讨论
  -「用户B」：发了一个有趣的AI生成图片，获得多人点赞

·今日热点话题
  [1] 技术架构升级方案（☆☆☆☆☆）
  - 内容摘要：从monolith迁移到微服务；讨论了服务拆分方案；评估了技术栈选择；计划了迁移时间表
  - 其他讨论：性能监控方案；灰度发布策略
  - 讨论时间：14:20 - 15:30
  
  [2] 用户反馈问题处理（☆☆☆）
  - 内容摘要：分析了最近用户投诉的主要问题；制定了响应策略；安排了修复优先级
  - 讨论时间：16:05 - 16:40

·待办清单
  - [开发组待办] 完成架构设计文档更新
  - [测试组待办] 准备下周的压力测试方案
  - [产品组待办] 整理用户反馈报告并分发给相关团队

·☑全文点评：今日讨论主要围绕系统架构升级和用户体验改进展开，团队展现出良好的协作精神和问题解决能力。建议尽快推进文档更新并加强各团队间的沟通协调。
```

## 🛠️ 安装指南

### 前置条件

- Python 3.8+
- AstrBot 0.1.0+
- 配置好的LLM访问服务(支持OpenAI API、DeepSeek API等)

### 安装方法

1. **通过pip安装**
   ```bash
   pip install astrbot-plugin-chatsummary
   ```

2. **从源码安装**
   ```bash
   git clone https://github.com/jokeryuyc/astrbot-enhanced-chatsummary.git
   cd astrbot-enhanced-chatsummary
   pip install -e .
   ```

3. **在AstrBot配置中启用插件**
   
   编辑AstrBot配置文件`config.json`，添加以下内容：
   ```json
   {
     "plugins": [
       {
         "name": "astrbot_plugin_chatsummary",
         "config": {
           "max_records": 300,
           "extract_image_text": false
         }
       }
     ]
   }
   ```

4. **重启AstrBot服务**
   ```bash
   systemctl restart astrbot  # 如果使用systemd管理
   # 或
   pm2 restart astrbot  # 如果使用pm2管理
   ```

## 🎮 使用指南

### 基本命令

| 命令 | 描述 |
|------|------|
| `/消息总结 <数量>` | 总结指定数量的最近消息 |
| `/消息总结 <数量> debug` | 启用调试模式(仅管理员可用) |

### 参数说明

- **数量**: 必填，整数类型，指定要获取的历史消息数量(10-300)
- **debug**: 可选，启用调试模式，输出原始聊天记录和提示词信息

### 使用示例

1. **基本用法**: 总结最近100条消息
   ```
   /消息总结 100
   ```

2. **调试模式**: 总结50条消息并启用调试模式(仅管理员)
   ```
   /消息总结 50 debug
   ```

## ⚙️ 配置详解

插件的配置文件位于`data/config/astrbot_plugin_chatsummary_config.json`，支持以下配置项：

| 配置项 | 类型 | 默认值 | 描述 |
|--------|------|--------|------|
| `prompt` | string | *预设提示词* | 指导LLM如何总结聊天记录的提示词 |
| `max_records` | integer | 300 | 单次可获取的最大聊天记录数量 |
| `extract_image_text` | boolean | false | 是否尝试提取图片中的文字(需服务端支持OCR) |
| `debug_mode.enabled` | boolean | false | 是否启用调试模式 |
| `debug_mode.log_level` | string | "info" | 日志级别(info/debug/warning/error) |

### 自定义提示词

可以通过修改`prompt`配置项来自定义总结的风格和内容。提示词使用结构化格式描述总结要求，包括：

- **角色定义**: 定义LLM扮演的角色(社群聊天记录总结分析师)
- **背景说明**: 说明总结的目的和要求
- **输出格式**: 指定总结的结构和格式要求
- **处理原则**: 提供隐私保护、信息去重等原则指导
- **示例展示**: 提供样例输出供模型参考

## 🔍 技术实现

### 插件架构

本插件基于AstrBot的插件框架开发，主要包含以下组件：

- **消息获取模块**: 负责从群聊历史中提取消息
- **消息解析模块**: 处理不同类型的消息内容(文本、图片、表情等)
- **LLM调用模块**: 封装对大语言模型的API调用
- **配置管理模块**: 管理插件配置和提示词
- **权限控制模块**: 管理调试模式的访问权限

### 处理流程

1. 接收用户命令并解析参数
2. 验证参数合法性和用户权限
3. 获取指定数量的群聊历史消息
4. 解析和格式化消息内容
5. 构造系统提示词和用户输入
6. 调用LLM生成总结内容
7. 返回格式化的总结结果

### LLM调用优化

本插件针对不同的LLM提供商(如OpenAI、DeepSeek等)做了适配优化，确保提示词能够正确传递，主要通过以下方式：

```python
# 使用系统消息+用户消息的标准格式
llm_response = await self.context.get_using_provider().text_chat(
    contexts=[
        {"role": "system", "content": prompt},  # 系统提示词
        {"role": "user", "content": msg}        # 用户消息内容
    ],
)
```

## 🧩 插件扩展

### 支持的消息类型

插件目前支持解析以下类型的消息：

- 文本消息
- JSON消息(如分享卡片)
- 表情消息
- 图片消息
- 文件消息
- 语音消息
- @提及消息

### 开发自定义处理器

如需扩展支持更多消息类型，可以修改`_extract_message_text`方法：

```python
def _extract_message_text(self, message_parts):
    """从消息段中提取文本内容"""
    message_text = ""
    
    for part in message_parts:
        # 添加自定义消息类型处理
        if part.get('type') == 'your_custom_type':
            message_text += f"[自定义类型] {处理逻辑} "
            
    return message_text
```

## 📊 性能考量

- **记录数量限制**: 默认限制为300条消息，以平衡总结质量和API调用开销
- **错误重试**: 对LLM调用失败实现了错误捕获和友好提示
- **长文本处理**: 调试模式下会截断过长的输出，避免消息溢出
- **异步处理**: 使用异步方式调用API，避免阻塞主线程

## 🔄 版本历史

| 版本 | 发布日期 | 主要变更 |
|------|----------|----------|
| v1.0.2 | 2025-03-22 | 修复LLM API调用问题，增强错误处理，扩展支持消息类型 |
| v1.0.1 | 2024-12-15 | 原始版本，由laopanmemz开发 |

## 🤝 贡献指南

我们欢迎社区成员对本项目做出贡献。如果你想参与贡献，请遵循以下步骤：

1. Fork本仓库
2. 创建你的特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交你的更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启一个Pull Request

### 代码规范

- 遵循PEP 8风格指南
- 添加适当的类型注解
- 为所有函数编写清晰的文档字符串
- 确保代码可读性和可维护性

## 📜 许可证

本项目采用 [GNU Affero General Public License v3.0](LICENSE) 开源许可证。这意味着如果你修改了代码并在网络上提供服务，必须公开源代码。

## 🙏 致谢

- 感谢原作者 [laopanmemz](https://github.com/laopanmemz) 创建的初始版本
- 感谢 [DeepSeek](https://www.deepseek.com/) 和 [通义灵码](https://tongyi.aliyun.com/) 提供的模型支持
- 感谢 [AstrBot](https://astrbot.app) 社区的支持与反馈

## 📞 联系方式

如有问题或建议，请通过以下方式联系我们：

- 提交 [GitHub Issues](https://github.com/jokeryuyc/astrbot-enhanced-chatsummary/issues)
- 加入 [AstrBot交流群](https://jq.qq.com/?_wv=1027&k=xxx)

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/laopanmemz">laopanmemz</a> and contributors
</p>
