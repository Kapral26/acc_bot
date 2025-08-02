from aiogram import types

from tg_bot.domains.russian_roulette.services import RussianRouletteService


async def russian_roulette(
    message: types.Message,
    russian_roulette_service: RussianRouletteService,
) -> None:
    print("russian_roulette called")
    try:
        bad_phrase = await russian_roulette_service.start(message)
    except Exception as e:
        await message.answer(f"Проблема при добавлении пользователя: {e}")
    else:
        await message.answer(bad_phrase.phrase)


async def tst(
    message: types.Message,
) -> None:
    await message.answer("hui")
