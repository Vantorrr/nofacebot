"""
User middleware for automatic user creation and management.
"""

from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from sqlalchemy.orm import Session

from app.services.user import UserService
from app.models.user import User
from app.core.logger import get_logger

logger = get_logger(__name__)


class UserMiddleware(BaseMiddleware):
    """Middleware for automatic user creation and management."""
    
    async def __call__(
        self,
        handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: Dict[str, Any],
    ) -> Any:
        """
        Process user data and provide user instance to handler.
        
        Args:
            handler: Next handler
            event: Update object
            data: Handler data
            
        Returns:
            Handler result
        """
        # Get database session from previous middleware
        db: Session = data.get("db")
        if not db:
            logger.error("Database session not found in middleware data")
            return await handler(event, data)
        
        # Extract Telegram user
        tg_user = None
        if hasattr(event, 'from_user'):
            tg_user = event.from_user
        elif hasattr(event, 'message') and event.message:
            tg_user = event.message.from_user
        
        if not tg_user:
            # No user found, continue without user data
            return await handler(event, data)
        
        # Skip bots
        if tg_user.is_bot:
            return await handler(event, data)
        
        try:
            # Create user service and get/create user
            user_service = UserService(db)
            user = user_service.get_or_create_user(tg_user)
            
            # Check if user is blocked
            if user.is_blocked:
                logger.warning(f"Blocked user {user.telegram_id} attempted to interact")
                # You can handle blocked users here (e.g., send a message or ignore)
                return
            
            # Add user and user service to handler data
            data["user"] = user
            data["user_service"] = user_service
            
            # Call next handler
            return await handler(event, data)
            
        except Exception as e:
            logger.error(f"Error in user middleware: {e}", exc_info=True)
            # Continue without user data on error
            return await handler(event, data) 