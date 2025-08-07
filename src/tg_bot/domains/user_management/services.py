import logging
from dataclasses import dataclass
from functools import wraps

from aiogram import types

from src.app.users.chats.schemas import UserChatSchema
from src.app.users.schemas import UsersCreateSchema
from src.tg_bot.domains.user_management.repository import UserBotRepository
from src.tg_bot.domains.user_management.schemas import UserChatCheckResponse


def extract_user_data(func):
    @wraps(func)
    async def wrapper(self, event: types.TelegramObject, *args, **kwargs):
        # Общий метод извлечения данных пользователя
        user = event.from_user
        chat = event.chat if hasattr(event, "chat") else event.message.chat

        user_data = UsersCreateSchema(
            id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            chat=UserChatSchema.model_validate(chat),
        )

        return await func(self, event, user_data, *args, **kwargs)

    return wrapper


@dataclass
class UserBotService:
    user_bot_repository: UserBotRepository
    logger: logging.Logger

    @extract_user_data
    async def register_user(
        self,
        event: types.TelegramObject,
        user_data: UsersCreateSchema,
    ) -> str:
        register_user_result = await self.user_bot_repository.register_user(user_data)
        return register_user_result

    @extract_user_data
    async def is_user_in_chat(
        self,
        event: types.TelegramObject,
        user_data: UsersCreateSchema,
    ) -> UserChatCheckResponse:
        is_user = await self.user_bot_repository.is_user_in_chat(user_data)
        return is_user
