from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    app_name: str = "Web Summarizer"
    version: str = "0.1.0"
    debug: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
    
    # API Keys
    dashscope_api_key: str = os.getenv("DASHSCOPE_API_KEY", "")
    qwen_model: str = os.getenv("QWEN_MODEL", "qwen-7b-chat")

@lru_cache()
def get_settings() -> Settings:
    return Settings()
