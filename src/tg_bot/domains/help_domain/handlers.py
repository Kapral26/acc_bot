from aiogram import types
from aiogram.filters import Command

from src.tg_bot.domains.help_domain import help_router


@help_router.message(Command("help"))
async def help_command(message: types.Message) -> None:
    """Обработчик команды /help."""
    help_text = """
    Доступные команды:
    /start - Начать работу с ботом
    /help - Получить справку по командам
    /track - Отследить информацию о пользователе
    """
    await message.answer(help_text.strip())
