"""
Configuration management using Pydantic Settings.
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Server
    host: str = "localhost"
    port: int = 8000
    debug: bool = True
    
    # Security
    secret_key: str = "dev-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 7
    
    # CORS
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # Rate Limiting
    rate_limit_per_minute: int = 100
    rate_limit_authenticated_per_minute: int = 1000
    
    # Resource Limits
    max_execution_time_seconds: int = 30
    max_memory_mb: int = 512
    max_dataframe_rows: int = 1000000
    max_file_size_mb: int = 100
    
    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_enabled: bool = False
    
    # Sandbox
    sandbox_enabled: bool = False
    sandbox_type: str = "docker"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()





