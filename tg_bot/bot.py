import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import Command

from app.settings.configs.settings import Settings
from tg_bot.core.storage import get_storage
from tg_bot.domains import commands
from tg_bot.domains.base.handlers import BaseHandlers
from tg_bot.domains.dependencies import (
    russian_roulette_service,
    user_bot_service,
)
from tg_bot.domains.russian_roulette.handlers import russian_roulette
from tg_bot.domains.user_management.handlers import UserHandlers

settings = Settings()


class TelegramBot:
    def __init__(self):
        self.bot = Bot(token=settings.bot_token.get_secret_value())
        self.storage = get_storage()
        self.dp = Dispatcher(storage=self.storage)
        self._register_handlers()
        self._register_depends()

    def _register_depends(self):
        self.dp["user_bot_service"] = user_bot_service
        self.dp["russian_roulette_service"] = russian_roulette_service

    def _register_handlers(self) -> None:
        for command, handler in commands.items():
            self.dp.message.register(handler, Command(command))

    async def on_shutdown(self) -> None:
        await self.storage.close()
        await self.dp.shutdown()

    async def start(self):
        # self.dp.message.middleware(LoggingMiddleware())
        try:
            await self.dp.start_polling(self.bot, skip_updates=True, timeout=1,  relax=0.1)
        except asyncio.CancelledError:
            await self.bot.session.close()
        finally:
            await self.storage.close()
            await self.bot.session.close()
