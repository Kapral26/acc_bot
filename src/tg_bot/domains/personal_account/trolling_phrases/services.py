from dataclasses import dataclass

from src.tg_bot.domains.personal_account.trolling_phrases.repository import (
    TrollingPhrasesRepository,
)


@dataclass
class TrollingPhrasesService:
    trolling_phrases_repository: TrollingPhrasesRepository

    async def get_all_phrases(self) -> list[str]:
        register_user_result = await self.trolling_phrases_repository.get_all_phrases()
        return register_user_result
