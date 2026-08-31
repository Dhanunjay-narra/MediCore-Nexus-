"""
MediCore Nexus - Application Configuration
Centralized settings management using Pydantic Settings
"""

import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    APP_NAME: str = "MediCore Nexus"
    APP_VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"

    # Security & Tokens
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY", "medicore_nexus_super_secret_jwt_signing_key_for_development_only_change_in_prod_2026"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    MAX_LOGIN_ATTEMPTS: int = 5
    LOCKOUT_DURATION_MINUTES: int = 15

    # Server & CORS
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"
    ]

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "sqlite+aiosqlite:///./medicore_nexus.db"
    )
    DB_ECHO: bool = False

    # Redis Cache & Queue
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # Clinical & AI Decision Parameters
    AI_CONFIDENCE_THRESHOLD: float = 0.85
    ENABLE_AI_CLINICAL_SUPPORT: bool = True
    ENABLE_PREDICTIVE_INVENTORY: bool = True
    DRUG_SAFETY_STRICT_MODE: bool = True
    FEFO_EXPIRY_THRESHOLD_DAYS: int = 90

    # Storage
    STORAGE_LOCAL_PATH: str = "./uploads"

    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "ignore"


settings = Settings()
