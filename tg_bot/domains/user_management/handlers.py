from aiogram import types

from tg_bot.domains.user_management.services import UserBotService


class UserHandlers:
    @staticmethod
    async def reg_user(
        message: types.Message, user_bot_service: UserBotService
    ) -> None:
        try:
            register_suer_result = await user_bot_service.register_user(message)
        except Exception as e:
            await message.answer(f"Проблема при добавлении пользователя: {e}")
        else:
            await message.answer(register_suer_result)
