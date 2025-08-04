from dishka import Provider, Scope, provide

from src.app.analytics.bad_phrase.service import BadPhraseService
from src.app.analytics.repository import AnalyticsRepository
from src.app.analytics.service import AnalyticsService
from src.app.settings.database.database import async_session_factory
from src.app.users.service import UserService


class AnalyticsProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_analytics_repository(self) -> AnalyticsRepository:
        return AnalyticsRepository(session_factory=async_session_factory)

    @provide(scope=Scope.REQUEST)
    def get_analytics_service(
        self,
        analytics_repository: AnalyticsRepository,
        user_service: UserService,
        bad_phrase_service: BadPhraseService,
    ) -> AnalyticsService:
        return AnalyticsService(
            analytics_repository=analytics_repository,
            user_service=user_service,
            bad_phrase_service=bad_phrase_service,
        )
