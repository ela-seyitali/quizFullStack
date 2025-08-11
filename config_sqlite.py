from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # SQLite için konfigürasyon (geliştirme aşamasında)
    database_url: str = "sqlite:///./quiz.db"
    
    # Security Configuration
    secret_key: str = "your-super-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Application Configuration
    debug: bool = True
    environment: str = "development"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

settings = Settings() 