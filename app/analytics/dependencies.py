from typing import Annotated

from fastapi import Depends

from app.analytics.repository import AnalyticsRepository
from app.analytics.service import AnalyticsService
from app.settings.database.database import async_session_factory


async def get_analytics_repository() -> AnalyticsRepository:
    return AnalyticsRepository(session_factory=async_session_factory)


def get_analytics_service(
    analytics_repository: Annotated[
        AnalyticsRepository, Depends(get_analytics_repository)
    ],
) -> AnalyticsService:
    return AnalyticsService(analytics_repository=analytics_repository)
