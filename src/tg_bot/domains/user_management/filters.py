
from aiogram.filters import BaseFilter
from aiogram.types import Message

from src.tg_bot.domains.user_management.services import UserBotService


class UserInChatFilter(BaseFilter):
    async def __call__(self, message: Message, user_bot_service: UserBotService) -> bool:
        # Получаем текущее время
        try:
            await user_bot_service.is_user_in_chat(message)
        except ValueError as e:
            filter_text = "Ты не зарегистрирован в этом чате, используй команду /reg_user."
            await message.answer(filter_text)
            return False
        else:
            return True
