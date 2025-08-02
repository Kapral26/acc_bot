
from aiogram import types
from aiogram.fsm.context import FSMContext

from tg_bot.domains.user_management.services import UserBotService


class UserHandlers:

    @staticmethod
    async def reg_user(
            message: types.Message,
            user_bot_service: UserBotService
    ) -> None:
        try:
            register_suer_result = await user_bot_service.register_user(message)
        except Exception as e:
            await message.answer(f"Проблема при добавлении пользователя: {e}")
        else:
            await message.answer(register_suer_result)


    @staticmethod
    async def track_command(
            message: types.Message,
            user_bot_service: UserBotService,
            state: FSMContext
    ) -> None:
        """Обработчик команды /track. Показывает информацию о пользователе."""
        user_data = await user_bot_service.extract_user_data(message)

        response = (
            f"Собрана информация о пользователе:\n"
            f"ID: {user_data.user_id}\n"
            f"Имя: {user_data.first_name}\n"
            f"Фамилия: {user_data.last_name}\n"
            f"Username: @{user_data.username}"
        )

        await message.answer(response)
