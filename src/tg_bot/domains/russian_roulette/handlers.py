from aiogram.filters import Command
from aiogram.types import Message

from src.tg_bot.domains.russian_roulette import russian_roulette_router
from src.tg_bot.domains.russian_roulette.keyboards import roulette_kb
from src.tg_bot.domains.user_management.filters import UserInChatFilter



# Регистрация хендлера с фильтром
@russian_roulette_router.message(Command("russian_roulette"), UserInChatFilter())
async def russian_roulette(message: Message) -> None:
    await message.answer(
        "Чтобы начать русскую рулетку, нажмите на кнопку:", reply_markup=roulette_kb
    )
