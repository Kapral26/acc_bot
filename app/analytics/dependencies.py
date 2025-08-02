from typing import Annotated

from fastapi import Depends

from app.analytics.bad_phrase.dependencies import get_bad_phrase_service
from app.analytics.bad_phrase.service import BadPhraseService
from app.analytics.repository import AnalyticsRepository
from app.analytics.service import AnalyticsService
from app.settings.database.database import async_session_factory
from app.users.dependencies import get_user_service
from app.users.service import UserService


async def get_analytics_repository() -> AnalyticsRepository:
    return AnalyticsRepository(session_factory=async_session_factory)


def get_analytics_service(
    analytics_repository: Annotated[
        AnalyticsRepository, Depends(get_analytics_repository)
    ],
    user_service: Annotated[UserService, Depends(get_user_service)],
    bad_phrase_service: Annotated[BadPhraseService, Depends(get_bad_phrase_service)],
) -> AnalyticsService:
    return AnalyticsService(
        analytics_repository=analytics_repository,
        user_service=user_service,
        bad_phrase_service=bad_phrase_service,
    )
