from setuptools import setup, find_packages
import os

# 读取README文件
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# 读取版本信息
version = "1.0.2"  # 默认版本
try:
    with open("metadata.yaml", "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("version:"):
                version = line.split(":")[1].strip().replace("v", "")
                break
except:
    pass

setup(
    name="astrbot-plugin-chatsummary",
    version=version,
    author="laopanmemz",
    author_email="laopanmemz@example.com",  # 替换为实际邮箱
    description="智能聊天记录总结插件，基于LLM生成结构化内容摘要",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jokeryuyc/astrbot-enhanced-chatsummary",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "astrbot>=0.1.0",
    ],
    entry_points={
        "astrbot.plugins": [
            "astrbot_plugin_chatsummary=main:ChatSummary",
        ],
    },
    package_data={
        "": ["data/config/*.json"],
    },
)
