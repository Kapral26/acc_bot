from aiogram import F
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from src.tg_bot.domains.russian_roulette import russian_roulette_router
from src.tg_bot.domains.russian_roulette.services import RussianRouletteService
from src.tg_bot.domains.user_management.filters import UserInChatFilter

TEXT_BUTTON = "Играть в русскую рулетку"


roulette_button = KeyboardButton(text=TEXT_BUTTON)
roulette_kb = ReplyKeyboardMarkup(keyboard=[[roulette_button]], resize_keyboard=True)


@russian_roulette_router.message(
    F.text == TEXT_BUTTON,
 #   TimeRangeFilter(8, 23),
    UserInChatFilter()
)
@inject
async def handle_roulette_game(
    message: Message,
    russian_roulette_service: FromDishka[RussianRouletteService],
):
    """Хендлер для отлова сообщение TEXT_BUTTON."""
    try:
        bad_phrase = await russian_roulette_service.start(message)
    except Exception as e:
        await message.answer(f"Проблема при запуске русской рулетки: {e}")
    else:
        await message.answer(bad_phrase.phrase)
