"""配置文件 - 管理API密钥和数据库连接配置"""
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# OpenAI API配置
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")  # 或使用Claude模型
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", None) 

# 数据库配置（伪代码 - 实际使用时需要配置真实连接信息）
DATABASE_CONFIG = {
    "type": os.getenv("DATABASE_TYPE", "mysql"),  # mysql 或 postgresql
    "host": os.getenv("DATABASE_HOST", "localhost"),
    "port": int(os.getenv("DATABASE_PORT", "3306")),
    "user": os.getenv("DATABASE_USER", "root"),
    "password": os.getenv("DATABASE_PASSWORD", ""),
    "database": os.getenv("DATABASE_NAME", "fitness_db"),
    "charset": os.getenv("DATABASE_CHARSET", "utf8mb4"),
}

# Agent配置
AGENT_CONFIG = {
    "max_iterations": 10,
    "temperature": 0.7,
}

