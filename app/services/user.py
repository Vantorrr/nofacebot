"""
User management service.
"""

from typing import Optional
from sqlalchemy.orm import Session
from aiogram.types import User as TgUser

from app.models.user import User
from app.core.logger import get_logger

logger = get_logger(__name__)


class UserService:
    """Service for managing users."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_or_create_user(self, tg_user: TgUser) -> User:
        """
        Get existing user or create new one from Telegram user data.
        
        Args:
            tg_user: Telegram user object
            
        Returns:
            User instance
        """
        user = self.db.query(User).filter(
            User.telegram_id == tg_user.id
        ).first()
        
        if not user:
            user = self.create_user(tg_user)
            logger.info(f"Created new user: {user.telegram_id}")
        else:
            # Update user info if changed
            self.update_user_info(user, tg_user)
        
        return user
    
    def create_user(self, tg_user: TgUser) -> User:
        """
        Create new user from Telegram user data.
        
        Args:
            tg_user: Telegram user object
            
        Returns:
            Created user instance
        """
        user = User(
            telegram_id=tg_user.id,
            username=tg_user.username,
            first_name=tg_user.first_name,
            last_name=tg_user.last_name,
            language_code=tg_user.language_code,
            is_bot=tg_user.is_bot,
            is_premium=getattr(tg_user, 'is_premium', False)
        )
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        return user
    
    def update_user_info(self, user: User, tg_user: TgUser) -> User:
        """
        Update user information from Telegram data.
        
        Args:
            user: Existing user instance
            tg_user: Telegram user object
            
        Returns:
            Updated user instance
        """
        updated = False
        
        if user.username != tg_user.username:
            user.username = tg_user.username
            updated = True
        
        if user.first_name != tg_user.first_name:
            user.first_name = tg_user.first_name
            updated = True
        
        if user.last_name != tg_user.last_name:
            user.last_name = tg_user.last_name
            updated = True
        
        if user.language_code != tg_user.language_code:
            user.language_code = tg_user.language_code
            updated = True
        
        premium = getattr(tg_user, 'is_premium', False)
        if user.is_premium != premium:
            user.is_premium = premium
            updated = True
        
        if updated:
            self.db.commit()
            logger.info(f"Updated user info: {user.telegram_id}")
        
        return user
    
    def get_user_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """
        Get user by Telegram ID.
        
        Args:
            telegram_id: Telegram user ID
            
        Returns:
            User instance if found, None otherwise
        """
        return self.db.query(User).filter(
            User.telegram_id == telegram_id
        ).first()
    
    def block_user(self, user: User) -> None:
        """
        Block user (mark as blocked).
        
        Args:
            user: User instance to block
        """
        user.is_blocked = True
        self.db.commit()
        logger.info(f"Blocked user: {user.telegram_id}")
    
    def unblock_user(self, user: User) -> None:
        """
        Unblock user.
        
        Args:
            user: User instance to unblock
        """
        user.is_blocked = False
        self.db.commit()
        logger.info(f"Unblocked user: {user.telegram_id}")
    
    def get_users_count(self) -> int:
        """
        Get total users count.
        
        Returns:
            Total number of users
        """
        return self.db.query(User).count()
    
    def get_all_users(self) -> list[User]:
        """
        Get all users.
        
        Returns:
            List of all users
        """
        return self.db.query(User).filter(
            User.is_blocked == False
        ).all() 