"""
Configuration settings for the Quiz API application.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application settings"""
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:101108aSy@localhost:5432/quiz_db")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    

    
    # Application
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Quiz API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "A comprehensive quiz application API"

# Global settings instance
settings = Settings()
