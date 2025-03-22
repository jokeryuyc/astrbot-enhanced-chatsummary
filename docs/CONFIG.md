# AstrBot 增强版聊天总结插件配置指南

本文档提供了插件的详细配置说明，使用者可根据需要进行自定义调整。

## 配置文件位置

主要配置文件存放在插件根目录的 `data/config/` 文件夹下：

- `config.json` - 主配置文件
- `prompts.json` - LLM 提示词配置
- `templates.json` - 输出模板配置

## 主配置项说明

### 基本配置

```json
{
  "command_trigger": "/消息总结",     // 命令触发关键词
  "default_count": 100,                // 默认总结消息数量
  "max_count": 500,                    // 最大允许总结消息数量
  "default_language": "zh-CN",         // 默认语言
  "admin_only": false,                  // 是否仅允许管理员使用
  "cooldown_seconds": 60,              // 命令冷却时间（秒）
  "enable_logging": true                // 是否启用日志记录
}
```

### 模型调用配置

```json
{
  "llm": {
    "provider": "openai",                // LLM 提供商，支持 openai、anthropic、gemini 等
    "model": "gpt-3.5-turbo",            // 使用的模型
    "api_key": "${OPENAI_API_KEY}",      // API 密钥，可使用环境变量
    "timeout": 30,                      // 调用超时时间（秒）
    "max_tokens": 2000,                 // 最大生成令牌数
    "temperature": 0.7                   // 生成温度，越低越确定性
  }
}
```

### 输出格式配置

```json
{
  "output": {
    "format": "markdown",                 // 输出格式，支持 markdown、text、html
    "template": "default",                // 使用的模板名称
    "max_length": 4000,                  // 最大输出长度
    "truncate_strategy": "smart"         // 截断策略：smart、end、none
  }
}
```

## 提示词配置

在 `prompts.json` 文件中可以自定义发送给 LLM 的提示词：

```json
{
  "default": {
    "system": "你是一个专业的群聊消息总结助手，擅长提取关键信息并进行结构化输出。请对以下聊天记录进行总结：",
    "user_template": "请对以下最近 {count} 条消息进行总结，提取关键信息：\n{messages}\n\n请以以下结构进行输出：\n1. 今日速览：概括最主要的1-3个讨论点\n2. 热门话题：按主题整理的讨论内容\n3. 小组任务：如有任务分配或待办事项请列出\n4. 精彩瞬间：有趣的对话或亮点发言"
  },
  "concise": {
    "system": "你是一个简洁的消息总结助手，请用最精炼的语言总结以下内容：",
    "user_template": "请对以下 {count} 条消息进行极简总结：\n{messages}\n\n请用不超过3个要点总结核心内容。"
  }
}
```

## 输出模板配置

在 `templates.json` 文件中可自定义输出模板：

```json
{
  "default": {
    "header": "# 📊 聊天记录总结\n\n*总结了最近 {count} 条消息 | 生成时间: {timestamp}*\n\n",
    "footer": "\n\n---\n*由 AstrBot 增强版聊天总结插件生成*"
  },
  "simple": {
    "header": "【聊天总结】\n\n",
    "footer": "\n\n- 总结了 {count} 条消息"
  }
}
```

## 国际化配置

插件支持多语言，语言文件位于 `i18n/` 目录下：

- `zh-CN.json` - 简体中文
- `en-US.json` - 英语（美国）
- `ja-JP.json` - 日语

可通过修改 `default_language` 配置或在命令中添加语言代码来切换语言：

```
/消息总结 100 en-US
```

## 高级配置选项

### 自定义消息过滤器

可在 `config.json` 中添加消息过滤规则：

```json
{
  "message_filters": {
    "ignore_system": true,               // 忽略系统消息
    "ignore_bot": true,                  // 忽略机器人消息
    "ignore_commands": true,             // 忽略命令消息
    "ignore_patterns": [                 // 忽略匹配正则表达式的消息
      "^/[a-zA-Z]+",
      "^https?://"
    ]
  }
}
```

### 调试模式配置

管理员可以启用调试模式获取更详细的信息：

```json
{
  "debug": {
    "enabled": false,                    // 是否默认启用
    "include_raw_messages": true,        // 包含原始消息
    "include_prompt": true,              // 包含发送给 LLM 的提示词
    "include_response": true             // 包含 LLM 的原始响应
  }
}
```

## 配置最佳实践

1. **性能优化**：
   - 合理设置 `max_count` 和 `max_tokens` 以避免超时
   - 对高频使用场景，考虑启用缓存机制

2. **安全考虑**：
   - 敏感信息（如 API 密钥）应使用环境变量
   - 考虑设置 `admin_only: true` 限制使用权限

3. **自定义建议**：
   - 根据群聊类型调整提示词以获取更相关的总结
   - 为不同场景（如学习讨论、项目协作）创建专用模板

## 故障排除

### 常见问题

1. **总结生成失败**
   - 检查 LLM 相关配置是否正确
   - 验证 API 密钥是否有效
   - 查看日志文件获取详细错误信息

2. **输出格式不符合预期**
   - 检查提示词配置是否清晰明确
   - 确认模板文件格式正确
   - 尝试调整 `temperature` 值

3. **插件无响应**
   - 确认触发命令格式正确
   - 检查权限设置
   - 确认没有触发冷却时间限制