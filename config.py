import os
from dotenv import load_dotenv

load_dotenv()  # 加载 .env 环境变量文件（如果你有）

# 数据库配置
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./silver_travel.db")

# 加密密钥
SECRET_KEY = os.getenv("SECRET_KEY", "your_super_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # Token 有效期：7天

# 微信小程序配置（如有）
WECHAT_APPID = os.getenv("WECHAT_APPID", "your_wechat_appid")
WECHAT_SECRET = os.getenv("WECHAT_SECRET", "WECHAT_SECRET")

DOUBAO_API_KEY = "f6d78d84-e1c1-47ae-b325-a7c01d1dd9d9"
LLM_OPTIONS = {
    "model": "doubao-1-5-pro-32k-250115",
    "type": "doubao",
    "temperature": 0.4,
    "max_tokens": 1500,
    "top_p": 1.0,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0
}