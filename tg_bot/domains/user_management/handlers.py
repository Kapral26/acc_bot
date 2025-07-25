import httpx
from aiogram import types
from aiogram.fsm.context import FSMContext

from .services import UserService


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
    async def reg_user(message: types.Message) -> None:
        user_data = UserService.extract_user_data(message)
        payload = {
            "username": user_data.username,
            "first_name": user_data.first_name,
            "last_name": user_data.last_name,
        }
        async with httpx.AsyncClient() as client:
            response = await client.post("http://localhost:8000/users/", json=payload)
            response.raise_for_status()
            return response.json()

    @staticmethod
    async def track_command(message: types.Message, state: FSMContext) -> None:
        """Обработчик команды /track. Показывает информацию о пользователе."""
        user_data = UserService.extract_user_data(message)

        response = (
            f"Собрана информация о пользователе:\n"
            f"ID: {user_data.user_id}\n"
            f"Имя: {user_data.first_name}\n"
            f"Фамилия: {user_data.last_name}\n"
            f"Username: @{user_data.username}"
        )

        await message.answer(response)
