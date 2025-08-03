from aiogram import types

from tg_bot.domains.russian_roulette.keyboards import roulette_kb


async def russian_roulette(
    message: types.Message,
) -> None:
    await message.answer(
        "Что бы начать русскую рулетку, нажмите на кнопку:", reply_markup=roulette_kb
    )
