from app.routers.health import router as health_router
from app.routers.watches import router as watches_router
from app.routers.collections import router as collections_router
from app.routers.search import router as search_router
from app.routers.statistics import router as statistics_router

__all__ = [
    "health_router",
    "watches_router",
    "collections_router",
    "search_router",
    "statistics_router",
]
