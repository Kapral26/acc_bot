import asyncio
import logging

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject


class RateLimitMiddleware(BaseMiddleware):
    def __init__(self, limit: int = 1, per_seconds: float = 2.5):
        self.limit = limit
        self.per_seconds = per_seconds
        self.timestamps = []

    async def __call__(self, handler, event: TelegramObject, data: dict):
        now = asyncio.get_event_loop().time()
        self.timestamps = [t for t in self.timestamps if t > now - self.per_seconds]

        if len(self.timestamps) >= self.limit:
            # Слишком много запросов — ждём
            await asyncio.sleep(self.per_seconds - (now - self.timestamps[0]))
            self.timestamps = [asyncio.get_event_loop().time()]

        self.timestamps.append(asyncio.get_event_loop().time())
        return await handler(event, data)


class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: TelegramObject, data: dict):
        logger = await data["dishka_container"].get(logging.Logger)
        start_time = asyncio.get_event_loop().time()
        result = await handler(event, data)
        duration = asyncio.get_event_loop().time() - start_time
        # Тип события и его содержимое
        if event.message and event.message.text:
            summary = f"{event.message.text.strip()} from {event.message.from_user.id}"
        elif event.callback_query:
            summary = f"callback '{event.callback_query.data}' from {event.callback_query.from_user.username}"
        else:
            summary = f"{event.event_type}"
        logger.info(f"Обработка {summary} события заняла {duration:.3f} сек")
        return result
