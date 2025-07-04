"""
Logging middleware for tracking user interactions.
"""

import time
from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware

from app.core.logger import get_logger

logger = get_logger(__name__)


class LoggingMiddleware(BaseMiddleware):
    """Middleware for logging user interactions."""
    
    async def __call__(
        self,
        handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: Dict[str, Any],
    ) -> Any:
        """
        Process update with logging.
        
        Args:
            handler: Next handler
            event: Update object
            data: Handler data
            
        Returns:
            Handler result
        """
        start_time = time.time()
        
        # Extract user and event info
        user_info = self._extract_user_info(event)
        event_info = self._extract_event_info(event)
        
        logger.info(
            f"Processing {event_info['type']} from user {user_info['id']} "
            f"(@{user_info['username']}) | Text: {event_info['text'][:100]}..."
        )
        
        try:
            # Call next handler
            result = await handler(event, data)
            
            # Log success
            duration = (time.time() - start_time) * 1000
            logger.info(
                f"Successfully processed {event_info['type']} "
                f"in {duration:.2f}ms"
            )
            
            return result
            
        except Exception as e:
            # Log error
            duration = (time.time() - start_time) * 1000
            logger.error(
                f"Error processing {event_info['type']} "
                f"after {duration:.2f}ms: {e}",
                exc_info=True
            )
            raise
    
    def _extract_user_info(self, event) -> Dict[str, Any]:
        """Extract user information from event."""
        user = None
        
        # Event is already a specific type (Message, CallbackQuery, etc.)
        if hasattr(event, 'from_user'):
            user = event.from_user
        elif hasattr(event, 'message') and hasattr(event.message, 'from_user'):
            user = event.message.from_user
        
        if user:
            return {
                "id": user.id,
                "username": user.username or "None",
                "first_name": user.first_name or "",
                "last_name": user.last_name or "",
                "is_bot": user.is_bot,
                "is_premium": getattr(user, 'is_premium', False)
            }
        
        return {"id": "unknown", "username": "unknown"}
    
    def _extract_event_info(self, event) -> Dict[str, Any]:
        """Extract event information from event."""
        from aiogram.types import Message, CallbackQuery, InlineQuery
        
        if isinstance(event, Message):
            return {
                "type": "message",
                "text": event.text or event.caption or "[media]",
                "chat_type": event.chat.type,
                "chat_id": event.chat.id
            }
        elif isinstance(event, CallbackQuery):
            return {
                "type": "callback",
                "text": event.data or "[no_data]",
                "chat_type": "callback",
                "chat_id": event.message.chat.id if event.message else None
            }
        elif isinstance(event, InlineQuery):
            return {
                "type": "inline_query",
                "text": event.query or "[empty]",
                "chat_type": "inline",
                "chat_id": None
            }
        
        return {
            "type": "unknown",
            "text": "[unknown_event]",
            "chat_type": "unknown",
            "chat_id": None
        } 