from dataclasses import dataclass

from src.tg_bot.core.api_adapter.service import APIAdapter


@dataclass
class UserAnalyticsRepository:
    api_adapter: APIAdapter

    async def get_user_statistic(self, user_id: int):
        response = await self.api_adapter.api_get(
            f"/russian_roulette/analytics/{user_id}",
        )
        response.raise_for_status()
        return response.json()
