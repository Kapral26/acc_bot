
from aiogram import types
from aiogram.fsm.context import FSMContext

from tg_bot.domains.user_management.services import UserBotService


class UserHandlers:
    @staticmethod
    async def start_command(message: types.Message) -> None:
        """Обработчик команды /start."""
        await message.answer("Привет! Я бот с базовыми командами. Используй /help для списка команд.")

    @staticmethod
    async def help_command(message: types.Message) -> None:
        """Обработчик команды /help."""
        help_text = """
        Доступные команды:
        /start - Начать работу с ботом
        /help - Получить справку по командам
        /track - Отследить информацию о пользователе
        """
        await message.answer(help_text.strip())

    @staticmethod
    async def reg_user(
            message: types.Message,
            user_bot_service: UserBotService
    ) -> None:
        try:
            user_data = await user_bot_service.extract_user_data(message)
            await user_bot_service.register_user(user_data)
        except Exception as e:
            await message.answer(f"Проблема при добавлении пользователя: {e}")
        else:
            response = (
                f"Пользователь зарегистрирован:\n"
                f"ID: {user_data.id}\n"
                f"Имя: {user_data.first_name}\n"
                f"Фамилия: {user_data.last_name}\n"
                f"Username: @{user_data.username}"
            )
            await message.answer(response)


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
