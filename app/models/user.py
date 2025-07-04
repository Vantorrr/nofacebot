"""
User model for storing user information.
"""

from sqlalchemy import Column, String, BigInteger, Boolean, DateTime
from sqlalchemy.orm import relationship

from .base import Base, TimestampMixin


class User(Base, TimestampMixin):
    """User model for storing Telegram user data."""
    
    __tablename__ = "users"
    
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True)
    username = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    language_code = Column(String(10), nullable=True)
    is_bot = Column(Boolean, default=False)
    is_premium = Column(Boolean, default=False)
    is_blocked = Column(Boolean, default=False)
    
    # Relationships
    applications = relationship("Application", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, username={self.username})>"
    
    @property
    def full_name(self) -> str:
        """Get user's full name."""
        parts = []
        if self.first_name:
            parts.append(self.first_name)
        if self.last_name:
            parts.append(self.last_name)
        return " ".join(parts) or self.username or f"User{self.telegram_id}"
    
    @property
    def mention(self) -> str:
        """Get user mention for Telegram."""
        if self.username:
            return f"@{self.username}"
        return f"<a href='tg://user?id={self.telegram_id}'>{self.full_name}</a>" 