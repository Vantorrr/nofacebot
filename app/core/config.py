"""
Configuration management with Pydantic validation.
"""

import os
from typing import List, Optional
from pydantic import validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with validation."""
    
    # Bot settings
    bot_token: str
    bot_name: str = "NOFACE.digital Bot"
    admin_ids: List[int] = []
    contact_username: str = "pavel_xdev"
    
    # Application settings
    debug: bool = False
    log_level: str = "INFO"
    webhook_host: Optional[str] = None
    webhook_port: int = 8080
    
    # Database
    database_url: str = "sqlite:///./app.db"
    
    # Services list
    services: List[str] = [
        "🌐 Сайты и веб-приложения",
        "📱 Telegram-боты", 
        "🛍 Интернет-магазины",
        "🎰 Казино и Web3",
        "🔐 Анонимные платформы",
        "🧠 AI-интеграции",
        "🚀 Стартапы под ключ"
    ]
    
    @validator('bot_token')
    def validate_bot_token(cls, v):
        """Validate bot token format."""
        if not v or ':' not in v:
            raise ValueError('Invalid bot token format')
        return v
    
    @validator('admin_ids', pre=True)
    def validate_admin_ids(cls, v):
        """Validate admin IDs - support both single int and list."""
        if v is None or v == "":
            return []
        if isinstance(v, int):
            return [v] if v > 0 else []
        if isinstance(v, str):
            # Support comma-separated values from .env
            ids = [int(x.strip()) for x in v.split(',') if x.strip()]
            return [id for id in ids if id > 0]
        if isinstance(v, list):
            return [id for id in v if isinstance(id, int) and id > 0]
        return []
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings() 