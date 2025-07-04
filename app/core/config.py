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
    admin_id: Optional[int] = None
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
    
    @validator('admin_id')
    def validate_admin_id(cls, v):
        """Validate admin ID."""
        if v is not None and v <= 0:
            raise ValueError('Admin ID must be positive')
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings() 