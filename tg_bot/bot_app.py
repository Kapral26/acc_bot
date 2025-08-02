from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from core.storage import get_storage
from domains.user_management.handlers import UserHandlers

from app.settings.configs.settings import Settings
from tg_bot.domains.base.handlers import BaseHandlers
from tg_bot.domains.dependencies import (
    russian_roulette_service,
    user_bot_service,
    user_info_service,
)
from tg_bot.domains.russian_roulette.handlers import russian_roulette

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
        self.dp["user_info_service"] = user_info_service
        print(self.dp["user_info_service"])

    def _register_handlers(self) -> None:
        self.dp.message.register(BaseHandlers.start_command, Command("start"))
        self.dp.message.register(BaseHandlers.help_command, Command("help"))
        self.dp.message.register(UserHandlers.reg_user, Command("reg_user"))
        self.dp.message.register(UserHandlers.track_command, Command("track"))
        self.dp.message.register(user_info, Command("user_info"))  # новый хендлер

        self.dp.message.register(russian_roulette, Command("russian_roulette"))

    async def on_shutdown(self, dp: Dispatcher) -> None:
        await self.storage.close()
        await self.storage.wait_closed()

    async def main(self):
        # self.dp.message.middleware(LoggingMiddleware())
        try:
            await self.dp.start_polling(self.bot)
        finally:
            await self.storage.close()
