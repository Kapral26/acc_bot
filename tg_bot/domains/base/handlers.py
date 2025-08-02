from aiogram import types


class BaseHandlers:
    @staticmethod
    async def start_command(
        message: types.Message,
    ) -> None:
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
