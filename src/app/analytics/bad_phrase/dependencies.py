from dishka import Provider, Scope, provide

from src.app.analytics.bad_phrase.repository import BadPhraseRepository
from src.app.analytics.bad_phrase.service import BadPhraseService
from src.app.settings.database.database import async_session_factory


class BadPhraseRepositoryProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_bad_phrase_repository(self) -> BadPhraseRepository:
        return BadPhraseRepository(session_factory=async_session_factory)

    async def get_bad_phrase_service(
        self,
        bad_phrase_repository: BadPhraseRepository,
    ) -> BadPhraseService:
        return BadPhraseService(bad_phrase_repository=bad_phrase_repository)
