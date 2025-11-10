# 健身记录分析Agent

基于LangGraph构建的智能健身记录分析系统，支持自然语言查询和分析运动数据。

## 功能特性

- 🤖 使用LangGraph构建的Agent架构
- 💬 自然语言查询支持（如"帮我看看今天的运动表现"）
- 📊 数据库读取和分析功能
- 🔍 智能意图识别和路由

## 项目结构

```
agent/
├── main.py                 # 主入口文件
├── config.py              # 配置文件
├── agents/                # Agent实现
├── tools/                 # 工具模块
├── database/              # 数据库模块
└── utils/                 # 工具函数
```

## 安装

```bash
pip install -r requirements.txt
```

## 配置

1. 复制 `.env.example` 为 `.env`
2. 配置OpenAI API密钥和数据库连接信息

## 使用

```bash
python main.py
```

## 技术栈

- Python 3.8+
- LangChain
- LangGraph
- OpenAI API (Claude)

