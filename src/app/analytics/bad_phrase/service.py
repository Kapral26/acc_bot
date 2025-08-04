# service.py — Сервисный слой для работы с запрещёнными фразами (BadPhrase)

from dataclasses import dataclass

from src.app.analytics.bad_phrase.models import BadPhrase
from src.app.analytics.bad_phrase.repository import BadPhraseRepository
from src.app.analytics.bad_phrase.schemas import BadPhraseCRUD, BadPhraseSchema


@dataclass
class BadPhraseService:
    bad_phrase_repository: BadPhraseRepository

    async def get_random_bad_phrase(self) -> BadPhrase :
        bad_phrase = await self.bad_phrase_repository.get_random_bad_phrase()
        return bad_phrase

    async def create_bad_phrase(self, bad_phrase: BadPhraseCRUD) -> BadPhraseSchema:
        new_bad_phrase = await self.bad_phrase_repository.create_bad_phrase(bad_phrase)
        return BadPhraseSchema.model_validate(new_bad_phrase)

    async def get_bad_phrase_by_id(self, bad_phrase_id: int) -> BadPhraseSchema:
        bad_phrase = await self.bad_phrase_repository.get_bad_phrase_by_id(
            bad_phrase_id
        )
        return BadPhraseSchema.model_validate(bad_phrase)

    async def get_bad_phrase_by_phrase(self, phrase: str) -> BadPhraseSchema:
        bad_phrase = await self.bad_phrase_repository.get_bad_phrase_by_phrase(phrase)
        return BadPhraseSchema.model_validate(bad_phrase)

    async def get_bad_phrases(self) -> list[BadPhraseSchema]:
        bad_phrases = await self.bad_phrase_repository.get_bad_phrases()
        return [BadPhraseSchema.model_validate(x) for x in bad_phrases]

    async def update_bad_phrase(
        self, bad_phrase_id: int, bad_phrase: BadPhraseCRUD
    ) -> BadPhraseSchema:
        db_bad_phrase = await self.bad_phrase_repository.update_bad_phrase(
            bad_phrase_id, bad_phrase
        )
        return BadPhraseSchema.model_validate(db_bad_phrase)

    async def delete_bad_phrase(self, bad_phrase_id: int):
        await self.bad_phrase_repository.delete_bad_phrase(bad_phrase_id)
