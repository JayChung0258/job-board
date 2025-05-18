from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Job Board API"
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./job_board.db")
    
    # CORS settings
    BACKEND_CORS_ORIGINS: list = ["*"]
    
    # JWT settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "secret_key_for_development")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    class Config:
        env_file = ".env"


settings = Settings()
