"""Bio-Forge Configuration"""

import os
from typing import List, Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置"""
    
    # 应用信息
    VERSION: str = "1.0.0"
    PROJECT_NAME: str = "Bio-Forge"
    CODENAME: str = "Genesis-2026"
    
    # API配置
    API_V1_STR: str = "/api/v1"
    
    # 安全
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # CORS
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # 数据库
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./data/bio-forge.db")
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # AI配置
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    
    # 智能体矩阵
    AGENT_MATRIX_SIZE: int = 120  # 120个分层智能体
    AGENT_LAYERS: int = 6  # 6层架构
    
    # 端口
    PORT: int = int(os.getenv("PORT", 1983))
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# 全局配置实例
settings = Settings()
