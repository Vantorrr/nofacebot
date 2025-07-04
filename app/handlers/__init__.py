"""
Modern handlers for the NOFACE.digital bot.
"""

from .start import router as start_router
from .services import services_router
from .team import router as team_router
from .admin import router as admin_router

# Export all routers - ORDER MATTERS! start_router должен быть последним
routers = [
    admin_router,
    services_router,
    team_router,
    start_router
]

__all__ = ['routers'] 