import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    应用配置类
    """
    # JWT配置
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # 数据库配置
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/db")
    
    # 应用配置
    PROJECT_NAME: str = "XinHuo API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "XinHuo Learning Platform API"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()