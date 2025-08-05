from aiogram import types
from aiogram.filters import Command

from src.tg_bot.domains.start_domain import start_router


@start_router.message(Command("start"))
async def start_command(
    message: types.Message,
) -> None:
    """Обработчик команды /start."""
    await message.answer(
        "Привет! Я бот с базовыми командами. Используй /help для списка команд."
    )
