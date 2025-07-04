"""
NOFACE.digital Telegram Bot - Professional Edition

A modern, scalable Telegram bot for managing service requests and team applications.
Built with enterprise-grade architecture and best practices.
"""

import asyncio
import sys
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

# Add app directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.config import settings
from app.core.logger import setup_logging, get_logger
from app.models.base import create_tables
from app.middlewares import DatabaseMiddleware, LoggingMiddleware, UserMiddleware
from app.handlers import routers


async def on_startup(bot: Bot) -> None:
    """
    Initialize bot on startup.
    
    Args:
        bot: Bot instance
    """
    logger = get_logger(__name__)
    
    # Create database tables
    try:
        create_tables()
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        raise
    
    # Get bot info
    bot_info = await bot.get_me()
    logger.info(
        f"Bot started successfully: @{bot_info.username} "
        f"({bot_info.first_name}) - ID: {bot_info.id}"
    )
    
    # Set bot commands
    from aiogram.types import BotCommand, BotCommandScopeDefault
    commands = [
        BotCommand(command="start", description="🚀 Запустить бота"),
        BotCommand(command="help", description="ℹ️ Помощь"),
        BotCommand(command="contact", description="📞 Контакты"),
        BotCommand(command="admin", description="👨‍💻 Админ-панель"),
    ]
    
    await bot.set_my_commands(commands, BotCommandScopeDefault())
    logger.info("Bot commands set successfully")


async def on_shutdown(bot: Bot) -> None:
    """
    Cleanup on bot shutdown.
    
    Args:
        bot: Bot instance
    """
    logger = get_logger(__name__)
    logger.info("Bot shutting down...")
    
    # Close bot session
    await bot.session.close()
    logger.info("Bot shutdown completed")


def create_bot() -> Bot:
    """
    Create and configure bot instance.
    
    Returns:
        Bot: Configured bot instance
    """
    return Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
            link_preview_is_disabled=True
        )
    )


def create_dispatcher() -> Dispatcher:
    """
    Create and configure dispatcher with middleware and routers.
    
    Returns:
        Dispatcher: Configured dispatcher
    """
    # Create dispatcher with memory storage
    dp = Dispatcher(storage=MemoryStorage())
    
    # Register middleware (order matters!)
    dp.message.middleware(LoggingMiddleware())
    dp.callback_query.middleware(LoggingMiddleware())
    
    dp.message.middleware(DatabaseMiddleware())
    dp.callback_query.middleware(DatabaseMiddleware())
    
    dp.message.middleware(UserMiddleware())
    dp.callback_query.middleware(UserMiddleware())
    
    # Register routers
    for router in routers:
        dp.include_router(router)
    
    # Register startup/shutdown handlers
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    return dp


async def main() -> None:
    """
    Main application entry point.
    """
    # Setup logging
    setup_logging(
        level=settings.log_level,
        enable_structured=not settings.debug
    )
    
    logger = get_logger(__name__)
    logger.info("Starting NOFACE.digital Bot...")
    
    # Validate configuration
    try:
        logger.info(f"Bot token: {settings.bot_token[:10]}...")
        logger.info(f"Admin ID: {settings.admin_id}")
        logger.info(f"Debug mode: {settings.debug}")
        logger.info(f"Database: {settings.database_url}")
    except Exception as e:
        logger.error(f"Configuration validation failed: {e}")
        return
    
    # Create bot and dispatcher
    bot = create_bot()
    dp = create_dispatcher()
    
    try:
        # Start polling
        logger.info("Starting bot polling...")
        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types(),
            drop_pending_updates=True
        )
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot stopped with error: {e}", exc_info=True)
    finally:
        await on_shutdown(bot)


if __name__ == "__main__":
    try:
        # Check Python version
        if sys.version_info < (3, 8):
            print("Error: Python 3.8+ is required")
            sys.exit(1)
        
        # Run main application
        asyncio.run(main())
        
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1) 