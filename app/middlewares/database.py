"""
Database middleware for providing database session.
"""

from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware

from app.models.base import SessionLocal, get_db
from app.core.logger import get_logger

logger = get_logger(__name__)


class DatabaseMiddleware(BaseMiddleware):
    """Middleware for providing database session to handlers."""
    
    async def __call__(
        self,
        handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: Dict[str, Any],
    ) -> Any:
        """
        Provide database session to handler.
        
        Args:
            handler: Next handler
            event: Update object
            data: Handler data
            
        Returns:
            Handler result
        """
        # Create database session
        db = SessionLocal()
        
        try:
            # Add session to handler data
            data["db"] = db
            
            # Call next handler
            result = await handler(event, data)
            
            # Commit any pending transactions
            db.commit()
            
            return result
            
        except Exception as e:
            # Rollback on error
            db.rollback()
            logger.error(f"Database transaction rolled back due to error: {e}")
            raise
            
        finally:
            # Always close the session
            db.close() 