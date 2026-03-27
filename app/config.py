"""DeerFlow 2.0 配置管理"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """应用配置"""
    app_name: str = "DeerFlow 2.0"
    app_env: str = "development"
    app_debug: bool = True
    app_url: str = "http://localhost:8000"
    api_prefix: str = "/api/v1"
    
    # 数据库
    database_url: str = "sqlite:///./deerflow.db"
    redis_url: str = "redis://localhost:6379/0"
    
    # Neo4j
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "deerflow123"
    
    # MinIO
    minio_endpoint: str = "localhost:9000"
    minio_access_key: str = "minioadmin"
    minio_secret_key: str = "minioadmin"
    minio_use_ssl: bool = False
    
    # Celery
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"
    
    # 安全
    secret_key: str = "your-secret-key-here-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440
    
    # 智能体
    max_agents: int = 120
    default_agent_timeout: int = 3600
    task_queue_size: int = 10000
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """获取配置单例"""
    return Settings()
