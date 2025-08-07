import re
from dataclasses import dataclass

from src.app.russian_roulette_analytics.bad_phrase.exceptions import PhraseAlreadyExist
from src.tg_bot.domains.personal_account.trolling_phrases.repository import (
    TrollingPhrasesRepository,
)


@dataclass
class TrollingPhrasesService:
    trolling_phrases_repository: TrollingPhrasesRepository

    async def get_all_phrases(self) -> list[str]:
        register_user_result = await self.trolling_phrases_repository.get_all_phrases()
        return register_user_result

    async def add_phrase(self, phrase: str):
        await self._validate_phrase(phrase)
        phrase = await self._clean_mention(phrase)
        new_phrase_message = await self.trolling_phrases_repository.add_phrase(phrase)
        if new_phrase_message:
            raise ValueError(new_phrase_message.json()["detail"])

    async def _validate_phrase(self, phrase: str) -> None:
        if "@" not in phrase:
            raise ValueError("Фраза обязательно должна содержать @")

    @staticmethod
    async def _clean_mention(text: str) -> str:
        """Оставляет только первую часть упоминания (до пробела или конца строки)"""
        return re.sub(r"(@)\w+.*", r"\1", text)

    async def preview_phrase(self, phrase: str, username: str) -> str:
        await self._validate_phrase(phrase)
        return phrase.replace("@", f"@{username}")
