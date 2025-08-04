from typing import Annotated

from dishka import FromDishka
from fastapi import Depends

from src.app.analytics.bad_phrase.repository import BadPhraseRepository
from src.app.analytics.repository import AnalyticsRepository
from src.app.analytics.service import AnalyticsService
from src.app.settings.database.database import async_session_factory
from src.app.users.dependencies import get_user_service
from src.app.users.service import UserService


async def get_analytics_repository() -> AnalyticsRepository:
    return AnalyticsRepository(session_factory=async_session_factory)


def get_analytics_service(
    analytics_repository: Annotated[
        AnalyticsRepository, Depends(get_analytics_repository)
    ],
    user_service: Annotated[UserService, Depends(get_user_service)],
    bad_phrase_service: FromDishka[BadPhraseRepository],
) -> AnalyticsService:
    return AnalyticsService(
        analytics_repository=analytics_repository,
        user_service=user_service,
        bad_phrase_service=bad_phrase_service,
    )
