from datetime import datetime

from aiogram.filters import BaseFilter
from aiogram.types import Message


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
                    f"{self.start_hour }:00-{self.end_hour}:00"
                )
            await message.answer(filter_text)
            return False
