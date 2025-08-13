from aiogram.filters import BaseFilter
from aiogram.types import Message
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from src.tg_bot.domains.user_management.services import UserBotService


class UserInChatFilter(BaseFilter):
    @inject
    async def __call__(
        self, message: Message, user_bot_service: FromDishka[UserBotService]
    ) -> bool:
        # Получаем текущее время
        user = await user_bot_service.is_user_in_chat(message)
        if not user.in_chat:
            filter_text = f"""
                @{message.from_user.username} - иди нахуй!
                Потом не забудь зарегистрироваться.
                'Основное меню' -> 'Зарегистрироваться'
                Для тупых: /reg_user
                """
            await message.answer(filter_text)
            return False
        else:
            return True
