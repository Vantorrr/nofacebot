"""
Advanced logging configuration for the bot.
"""

import sys
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

import structlog
from aiogram import loggers

from .config import settings


class ColoredFormatter(logging.Formatter):
    """Colored console formatter."""
    
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green  
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'      # Reset
    }
    
    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        record.levelname = f"{log_color}{record.levelname}{self.COLORS['RESET']}"
        return super().format(record)


def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    enable_structured: bool = True
) -> None:
    """
    Configure logging for the application.
    
    Args:
        level: Logging level
        log_file: Optional log file path
        enable_structured: Enable structured logging
    """
    
    # Create logs directory
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))
    
    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Console handler with colors
    console_handler = logging.StreamHandler(sys.stdout)
    console_formatter = ColoredFormatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # File handler
    if log_file or not settings.debug:
        log_file = log_file or f"logs/bot_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(name)s:%(lineno)d | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)
    
    # Configure aiogram loggers
    loggers.event.setLevel(logging.INFO)
    loggers.middlewares.setLevel(logging.INFO)
    loggers.dispatcher.setLevel(logging.INFO)
    
    # Structured logging
    if enable_structured:
        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                structlog.processors.JSONRenderer()
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )


def get_logger(name: str) -> logging.Logger:
    """Get logger instance."""
    return logging.getLogger(name) 