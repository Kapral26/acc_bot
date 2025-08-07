from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.app.russian_roulette_analytics.bad_phrase.service import BadPhraseService
from src.app.russian_roulette_analytics.repository import AnalyticsRepository
from src.app.russian_roulette_analytics.service import AnalyticsService
from src.app.users.service import UserService


class AnalyticsProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_analytics_repository(
        self,
        session_factory: async_sessionmaker
    ) -> AnalyticsRepository:
        return AnalyticsRepository(session_factory=session_factory)

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
