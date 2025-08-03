from dataclasses import dataclass

from app.users.schemas import UsersCreateSchema
from tg_bot.domains.api_adapter.service import APIAdapter


@dataclass
class UserBotRepository:
    api_adapter: APIAdapter

    async def register_user(self, user_data: UsersCreateSchema) -> str:
        register_suer_result = await self.api_adapter.api_post(
            "http://localhost:8000/users/", data=user_data.model_dump(mode="json")
        )
        resp = register_suer_result.json()
        return resp.get("detail") or resp.get("text")

    async def change_role(self, user_data: UsersCreateSchema):
        await self.api_adapter.api_post(
            "http://localhost:8000/users/", data=user_data.model_dump(mode="json")
        )

