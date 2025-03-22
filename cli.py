#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Enhanced Chat Summary CLI Tool

命令行工具，允许直接从终端使用聊天总结功能
"""

import os
import sys
import json
import argparse
import logging
from typing import Dict, Any, Optional

# 添加项目根目录到系统路径
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# 导入主模块
from main import EnhancedChatSummary
from i18n.i18n import get_i18n_manager, _

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("chat_summary_cli")


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    加载配置文件
    
    Args:
        config_path: 配置文件路径，如果为 None 则使用默认配置
        
    Returns:
        加载的配置字典
    """
    default_config = {
        "language": "en_US",
        "summary_format": "markdown",
        "summary_length": "medium",
        "include_timestamps": True,
        "include_participants": True,
        "highlight_keywords": True,
        "auto_save": False,
        "save_directory": "./summaries",
        "max_message_count": 100,
        "ignore_system_messages": True,
        "advanced": {
            "debug_mode": False,
            "custom_templates_dir": "",
            "api_timeout": 30
        }
    }
    
    if not config_path:
        # 如果没有提供配置文件路径，尝试加载默认配置
        default_config_path = os.path.join(
            os.path.dirname(__file__), 
            "data", "config", "default_config.json"
        )
        if os.path.exists(default_config_path):
            config_path = default_config_path
    
    if config_path and os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
                logger.info(f"Loaded configuration from {config_path}")
                return config
        except Exception as e:
            logger.error(f"Error loading configuration from {config_path}: {str(e)}")
    
    logger.info("Using default configuration")
    return default_config


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description=_("Enhanced Chat Summary CLI Tool")
    )
    
    parser.add_argument(
        "input_file", 
        help=_("Input chat log file path")
    )
    
    parser.add_argument(
        "-o", "--output", 
        help=_("Output file path"), 
        default=None
    )
    
    parser.add_argument(
        "-f", "--format",
        help=_("Output format (markdown, html, plain)"),
        choices=["markdown", "html", "plain"],
        default=None
    )
    
    parser.add_argument(
        "-l", "--language",
        help=_("Language for the summary"),
        choices=["en_US", "zh_CN"],
        default=None
    )
    
    parser.add_argument(
        "-c", "--config",
        help=_("Path to configuration file"),
        default=None
    )
    
    parser.add_argument(
        "-v", "--verbose",
        help=_("Enable verbose logging"),
        action="store_true"
    )
    
    return parser.parse_args()


def main():
    """主函数"""
    # 解析命令行参数
    args = parse_arguments()
    
    # 设置日志级别
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Verbose logging enabled")
    
    # 加载配置
    config = load_config(args.config)
    
    # 使用命令行参数覆盖配置文件设置
    if args.language:
        config["language"] = args.language
    
    if args.format:
        config["summary_format"] = args.format
    
    # 如果设置了语言，初始化i18n
    get_i18n_manager(config["language"])
    
    # 检查输入文件
    if not os.path.exists(args.input_file):
        logger.error(_("Input file not found: {}").format(args.input_file))
        sys.exit(1)
    
    # 设置输出文件
    output_file = args.output
    if not output_file:
        # 根据输入文件名和格式生成输出文件名
        base_name = os.path.splitext(os.path.basename(args.input_file))[0]
        ext = ".md" if config["summary_format"] == "markdown" else ".html" if config["summary_format"] == "html" else ".txt"
        output_file = f"{base_name}_summary{ext}"
    
    # 创建总结实例
    summarizer = EnhancedChatSummary(config)
    
    try:
        # 读取输入文件
        with open(args.input_file, "r", encoding="utf-8") as f:
            chat_data = f.read()
        
        # 生成聊天摘要
        logger.info(_("Generating summary for {}").format(args.input_file))
        summary = summarizer.generate_summary(chat_data)
        
        # 保存到文件
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(summary)
        
        logger.info(_("Summary saved to {}").format(output_file))
        
        # 打印成功信息
        print(_("Summary successfully generated and saved to {}").format(output_file))
        
    except Exception as e:
        logger.error(_("Error generating summary: {}").format(str(e)))
        sys.exit(1)


if __name__ == "__main__":
    main()
