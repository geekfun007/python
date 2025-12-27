"""应用配置管理"""
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List


class Settings(BaseSettings):
    """应用配置类
    
    使用 pydantic-settings 管理配置，支持从环境变量和 .env 文件读取
    """
    
    # 应用配置
    app_name: str = "FastAPI Demo"
    debug: bool = False
    api_v1_prefix: str = "/api/v1"
    
    # 数据库配置
    database_url: str = "sqlite:///./app.db"
    
    # JWT 配置
    secret_key: str = "your-secret-key-change-this"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # CORS 配置
    cors_origins: List[str] = ["http://localhost:3000"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """获取配置单例
    
    使用 lru_cache 确保只创建一次 Settings 实例
    """
    return Settings()


# 导出配置实例
settings = get_settings()
