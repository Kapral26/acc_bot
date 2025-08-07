from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.app.russian_roulette_analytics.bad_phrase.repository import BadPhraseRepository
from src.app.russian_roulette_analytics.bad_phrase.service import BadPhraseService


class BadPhraseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_bad_phrase_repository(
            self,
            session_factory: async_sessionmaker
    ) -> BadPhraseRepository:
        return BadPhraseRepository(session_factory=session_factory)

    @provide(scope=Scope.REQUEST)
    async def get_bad_phrase_service(
        self,
        bad_phrase_repository: BadPhraseRepository,
    ) -> BadPhraseService:
        return BadPhraseService(bad_phrase_repository=bad_phrase_repository)
