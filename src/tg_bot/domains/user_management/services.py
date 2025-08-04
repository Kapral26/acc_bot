from dataclasses import dataclass
from functools import wraps

from aiogram import types

from src.app.users.chats.schemas import UserChatSchema
from src.app.users.schemas import UsersCreateSchema
from src.tg_bot.domains.user_management.repository import UserBotRepository


def extract_user_data(func):
    @wraps(func)
    async def wrapper(self, message: types.Message, *args, **kwargs):
        # Извлечение данных пользователя
        user = message.from_user
        user_data = UsersCreateSchema(
            id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            chat=UserChatSchema.model_validate(message.chat),
        )
        # Передаем user_data в оригинальную функцию
        return await func(self, message, user_data, *args, **kwargs)

    return wrapper


@dataclass
class UserBotService:
    user_bot_repository: UserBotRepository

    # @staticmethod
    # async def extract_user_data(message: types.Message) -> UsersCreateSchema:
    #     user = message.from_user
    #     return UsersCreateSchema(
    #         id=user.id,
    #         username=user.username,
    #         first_name=user.first_name,
    #         last_name=user.last_name,
    #         chat=UserChatSchema.model_validate(message.chat),
    #     )
    @extract_user_data
    async def register_user(
        self, message: types.Message, user_data: UsersCreateSchema
    ) -> str:
        register_user_result = await self.user_bot_repository.register_user(user_data)
        return register_user_result

    @extract_user_data
    async def is_user_in_chat(
        self, message: types.Message, user_data: UsersCreateSchema
    ) -> None:
        is_user = await self.user_bot_repository.is_user_in_chat(user_data)
        if not is_user.in_chat:
            raise ValueError(is_user.detail)
