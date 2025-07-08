from decouple import config
from typing import Optional

class Settings:
    # Database
    DATABASE_URL: str = config("DATABASE_URL", default="sqlite:///./tours_management.db")
    
    # JWT Settings
    SECRET_KEY: str = config("SECRET_KEY", default="your-secret-key-change-in-production-please")
    ALGORITHM: str = config("ALGORITHM", default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = config("ACCESS_TOKEN_EXPIRE_MINUTES", default=30, cast=int)
    
    # Security
    BCRYPT_ROUNDS: int = config("BCRYPT_ROUNDS", default=12, cast=int)
    
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Tours Management API"
    VERSION: str = "1.0.0"
    
    # CORS
    BACKEND_CORS_ORIGINS: list = config(
        "BACKEND_CORS_ORIGINS", 
        default="http://localhost:3000,http://localhost:8080", 
        cast=lambda v: [i.strip() for i in v.split(",")]
    )

settings = Settings()
