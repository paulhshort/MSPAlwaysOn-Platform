"""
Configuration module for MSPAlwaysOn.
"""

import os
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, validator

class Settings(BaseSettings):
    """Application settings."""
    
    # API configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "MSPAlwaysOn"
    
    # CORS configuration
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        """Assemble CORS origins from string or list."""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # Database configuration
    DATABASE_URL: str = os.environ.get(
        "DATABASE_URL", "postgresql+asyncpg://postgres:postgres@db:5432/mspalwayson"
    )
    
    # Redis configuration
    REDIS_URL: str = os.environ.get("REDIS_URL", "redis://redis:6379/0")
    
    # JWT configuration
    JWT_SECRET_KEY: str = os.environ.get(
        "JWT_SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    )
    JWT_PUBLIC_KEY: str = os.environ.get("JWT_PUBLIC_KEY", "")
    JWT_ALGORITHM: str = "RS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # Azure AD configuration
    AZURE_AD_TENANT_ID: str = os.environ.get("AZURE_AD_TENANT_ID", "")
    AZURE_AD_CLIENT_ID: str = os.environ.get("AZURE_AD_CLIENT_ID", "")
    AZURE_AD_CLIENT_SECRET: str = os.environ.get("AZURE_AD_CLIENT_SECRET", "")
    
    # Alert Engine configuration
    ALERT_ENGINE_URL: str = os.environ.get("ALERT_ENGINE_URL", "http://alert-engine:8080")
    
    # Vault configuration
    VAULT_ADDR: str = os.environ.get("VAULT_ADDR", "http://vault:8200")
    VAULT_TOKEN: str = os.environ.get("VAULT_TOKEN", "mspalwayson-dev-token")
    
    class Config:
        """Pydantic config."""
        case_sensitive = True
        env_file = ".env"

# Create settings instance
settings = Settings()
