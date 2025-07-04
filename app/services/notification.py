"""
Notification service for sending messages to admins.
"""

from typing import Optional, List
from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError, TelegramNotFound

from app.models.application import Application
from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class NotificationService:
    """Service for sending notifications."""
    
    def __init__(self, bot: Bot):
        self.bot = bot
    
    async def send_application_notification(
        self,
        application: Application,
        admin_ids: Optional[List[int]] = None
    ) -> bool:
        """
        Send application notification to admin(s).
        
        Args:
            application: Application instance
            admin_ids: Optional list of admin IDs (uses config if not provided)
            
        Returns:
            True if at least one notification was sent successfully
        """
        if not admin_ids:
            if not settings.admin_id:
                logger.warning("No admin ID configured for notifications")
                return False
            admin_ids = [settings.admin_id]
        
        message = application.to_admin_message()
        success_count = 0
        
        for admin_id in admin_ids:
            try:
                await self.bot.send_message(
                    chat_id=admin_id,
                    text=message,
                    parse_mode="HTML",
                    disable_web_page_preview=True
                )
                success_count += 1
                logger.info(f"Sent application notification to admin {admin_id}")
                
            except TelegramForbiddenError:
                logger.warning(f"Admin {admin_id} blocked the bot")
            except TelegramNotFound:
                logger.warning(f"Admin {admin_id} not found")
            except Exception as e:
                logger.error(f"Failed to send notification to admin {admin_id}: {e}")
        
        if success_count > 0:
            logger.info(f"Successfully sent {success_count} notifications for application #{application.id}")
            return True
        else:
            logger.error(f"Failed to send any notifications for application #{application.id}")
            return False
    
    async def send_admin_message(
        self,
        message: str,
        admin_ids: Optional[List[int]] = None,
        parse_mode: str = "HTML"
    ) -> int:
        """
        Send custom message to admin(s).
        
        Args:
            message: Message text
            admin_ids: Optional list of admin IDs
            parse_mode: Message parse mode
            
        Returns:
            Number of successfully sent messages
        """
        if not admin_ids:
            if not settings.admin_id:
                logger.warning("No admin ID configured")
                return 0
            admin_ids = [settings.admin_id]
        
        success_count = 0
        
        for admin_id in admin_ids:
            try:
                await self.bot.send_message(
                    chat_id=admin_id,
                    text=message,
                    parse_mode=parse_mode,
                    disable_web_page_preview=True
                )
                success_count += 1
                
            except Exception as e:
                logger.error(f"Failed to send message to admin {admin_id}: {e}")
        
        return success_count
    
    async def broadcast_to_admins(
        self,
        message: str,
        admin_ids: Optional[List[int]] = None
    ) -> dict:
        """
        Broadcast message to all admins with detailed results.
        
        Args:
            message: Message to broadcast
            admin_ids: Optional list of admin IDs
            
        Returns:
            Dictionary with broadcast results
        """
        if not admin_ids:
            if not settings.admin_id:
                return {"success": 0, "failed": 0, "errors": ["No admin ID configured"]}
            admin_ids = [settings.admin_id]
        
        results = {
            "success": 0,
            "failed": 0,
            "errors": []
        }
        
        for admin_id in admin_ids:
            try:
                await self.bot.send_message(
                    chat_id=admin_id,
                    text=message,
                    parse_mode="HTML",
                    disable_web_page_preview=True
                )
                results["success"] += 1
                
            except Exception as e:
                results["failed"] += 1
                results["errors"].append(f"Admin {admin_id}: {str(e)}")
        
        logger.info(
            f"Broadcast completed: {results['success']} success, "
            f"{results['failed']} failed"
        )
        
        return results 