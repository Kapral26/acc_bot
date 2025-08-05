from dataclasses import dataclass

from starlette import status

from src.app.users.schemas import UsersCreateSchema
from src.tg_bot.core.api_adapter.service import APIAdapter
from src.tg_bot.domains.user_management.schemas import UserChatCheckResponse


@dataclass
class UserBotRepository:
    api_adapter: APIAdapter

    async def register_user(self, user_data: UsersCreateSchema) -> str:
        response = await self.api_adapter.api_post(
            "/users/", data=user_data.model_dump(mode="json")
        )
        if response.status_code != status.HTTP_201_CREATED:
            response_text = response.json().get("detail")
        else:
            response_text = "Зарегистрирован.✅"
        return response_text

    async def change_role(self, user_data: UsersCreateSchema):
        await self.api_adapter.api_post(
            "/users/", data=user_data.model_dump(mode="json")
        )

    async def is_user_in_chat(
        self, user_data: UsersCreateSchema
    ) -> UserChatCheckResponse:
        response = await self.api_adapter.api_get(
            f"/chats/{user_data.chat.id}/users/{user_data.id}"
        )
        return UserChatCheckResponse(
            in_chat=response.status_code == status.HTTP_200_OK,
            detail=response.json().get("detail")
            if response.status_code != 200
            else None,
        )
