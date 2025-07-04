"""
Database models for the NOFACE.digital bot.
"""

from .application import Application, ApplicationType
from .user import User

__all__ = ['Application', 'ApplicationType', 'User'] 