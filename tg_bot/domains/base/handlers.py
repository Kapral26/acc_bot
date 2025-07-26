from aiogram import types
from tg_bot.domains.user_management.handlers import UserHandlers
from tg_bot.domains.user_management.services import UserBotService


class BaseHandlers:
    @staticmethod
    async def start_command(
        message: types.Message,
        user_bot_service: UserBotService,
    ) -> None:
        """Обработчик команды /start."""
        await UserHandlers.reg_user(message, user_bot_service)
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
