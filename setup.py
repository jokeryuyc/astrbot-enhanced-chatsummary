from setuptools import setup, find_packages
import os

# 读取README文件
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# 读取版本信息
version = "1.0.3"  # 默认版本
try:
    with open("metadata.yaml", "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("version:"):
                version = line.split(":")[1].strip().replace("v", "")
                break
except:
    pass

# 获取依赖项
requirements = [
    "astrbot>=0.1.0",
    "jinja2>=3.0.0",
    "pyyaml>=6.0.0",
    "typing-extensions>=4.0.0"
]

# 开发依赖项
extras_require = {
    "dev": [
        "pytest>=6.0.0",
        "pytest-asyncio>=0.16.0",
        "pytest-cov>=2.12.0",
        "black>=21.5b0",
        "flake8>=3.9.0",
        "mypy>=0.812"
    ]
}

setup(
    name="astrbot-plugin-chatsummary",
    version=version,
    author="jokeryuyc",
    author_email="jokeryuyc@example.com",  # 替换为实际邮箱
    description="增强版聊天记录总结插件，支持多语言和更多功能",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jokeryuyc/astrbot-enhanced-chatsummary",
    packages=find_packages(include=["i18n", "i18n.*"]),
    py_modules=["main", "cli"],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require=extras_require,
    entry_points={
        "astrbot.plugins": [
            "astrbot_enhanced_chatsummary=main:EnhancedChatSummary",
        ],
        "console_scripts": [
            "astrbot-summarize=cli:main",
        ],
    },
    package_data={
        "": [
            "data/config/*.json",
            "data/templates/*.md",
            "data/templates/*.html",
            "i18n/*.json"
        ],
    },
)
