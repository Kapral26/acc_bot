from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from core.storage import get_storage
from domains.user_management.handlers import UserHandlers

from app.settings.configs.settings import Settings

settings = Settings()

class TelegramBot:
    def __init__(self):
        self.bot = Bot(token=settings.bot_token.get_secret_value())
        self.storage = get_storage()
        self.dp = Dispatcher(storage=self.storage)
        self._register_handlers()

    def _register_handlers(self) -> None:
        self.dp.message.register(
            UserHandlers.start_command,
            Command("start")
        )
        self.dp.message.register(
            UserHandlers.help_command,
            Command("help")
        )
        self.dp.message.register(
            UserHandlers.reg_user,
            Command("reg_user")
        )
        self.dp.message.register(
            UserHandlers.track_command,
            Command("track")
        )

    async def on_shutdown(self, dp: Dispatcher) -> None:
        await self.storage.close()
        await self.storage.wait_closed()

    async def main(self):

        try:
            await self.dp.start_polling(self.bot)
        finally:
            await self.storage.close()

