from dataclasses import dataclass

from httpx import Response

from src.app.russian_roulette_analytics.bad_phrase.schemas import BadPhraseCRUD
from src.tg_bot.core.api_adapter.service import APIAdapter


@dataclass
class TrollingPhrasesRepository:
    api_adapter: APIAdapter

    async def get_all_phrases(self) -> list[str]:
        response = await self.api_adapter.api_get("/bad-phrases/")
        response.raise_for_status()
        return response.json()

    async def add_phrase(self, phrase_text: str) -> Response | None:
        data = BadPhraseCRUD(phrase=phrase_text).model_dump()
        response = await self.api_adapter.api_post(
            "/bad-phrases/",
            data=data,
        )
        if response.status_code == 409:
            return response

        response.raise_for_status()
        return None
