from typing import Annotated

from fastapi import Depends

from app.analytics.bad_phrase.repository import BadPhraseRepository
from app.analytics.bad_phrase.service import BadPhraseService
from app.settings.database.database import async_session_factory


async def get_bad_phrase_repository() -> BadPhraseRepository:
    return BadPhraseRepository(session_factory=async_session_factory)


def get_bad_phrase_service(
    bad_phrase_repository: Annotated[
        BadPhraseRepository, Depends(get_bad_phrase_repository)
    ],
) -> BadPhraseService:
    return BadPhraseService(bad_phrase_repository=bad_phrase_repository)
