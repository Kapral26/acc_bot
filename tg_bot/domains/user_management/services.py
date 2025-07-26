from dataclasses import dataclass

from aiogram import types
from app.users.chats.schemas import UserChatSchema
from app.users.schemas import UsersCreateSchema
from tg_bot.domains.user_management.repository import UserBotRepository


@dataclass
class UserBotService:
    user_bot_repository: UserBotRepository

    @staticmethod
    async def extract_user_data(message: types.Message) -> UsersCreateSchema:
        user = message.from_user
        return UsersCreateSchema(
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            chat=UserChatSchema.model_validate(message.chat)
        )

    async def register_user(self, message: types.Message) -> None:
        user_data = await self.extract_user_data(message)
        await self.user_bot_repository.register_user(user_data)

    async def set_admin_role(self, user_data: UsersCreateSchema) -> None:
        await self.user_bot_repository.change_role(user_data)
