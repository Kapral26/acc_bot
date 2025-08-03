from datetime import datetime

from aiogram import F, Router
from aiogram.filters import BaseFilter
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup

from tg_bot.domains.russian_roulette.services import RussianRouletteService

TEXT_BUTTON = "Играть в русскую рулетку"

router = Router()
roulette_button = KeyboardButton(text=TEXT_BUTTON)
roulette_kb = ReplyKeyboardMarkup(keyboard=[[roulette_button]], resize_keyboard=True)
active_tasks = set()



class TimeRangeFilter(BaseFilter):
    def __init__(self, start_hour: int, end_hour: int):
        self.start_hour = start_hour
        self.end_hour = end_hour

    async def __call__(self, message: Message) -> bool:
        # Получаем текущее время
        current_time = datetime.now().time()

        # Проверяем, попадает ли текущее время в диапазон
        if self.start_hour <= current_time.hour < self.end_hour:
            return True
        else:
            filter_text = (
                    f"@{message.from_user.username}, К вам выехали чеченцы, ибо нехуй!\n Рулетка работает "
                    f"8:00-23:00"
                )
            await message.answer(filter_text)
            return False


@router.message(F.text == TEXT_BUTTON, TimeRangeFilter(8, 23))
async def handle_roulette_game(
    message: Message,
    russian_roulette_service: RussianRouletteService,
):
    try:
        bad_phrase = await russian_roulette_service.start(message)
    except Exception as e:
        await message.answer(f"Проблема при запуске русской рулетки: {e}")
    else:
        await message.answer(bad_phrase.phrase)
