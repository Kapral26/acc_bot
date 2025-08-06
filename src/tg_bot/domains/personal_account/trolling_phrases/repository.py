from dataclasses import dataclass

from starlette import status

from src.app.users.schemas import UsersCreateSchema
from src.tg_bot.core.api_adapter.service import APIAdapter
from src.tg_bot.domains.user_management.schemas import UserChatCheckResponse


@dataclass
class TrollingPhrasesRepository:
    api_adapter: APIAdapter

    async def get_all_phrases(self) -> list[str]:
        response = await self.api_adapter.api_get("/bad-phrases/")
        response.raise_for_status()
        return response.json()