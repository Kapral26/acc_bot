import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from dishka.integrations.aiogram import setup_dishka

from src.app.settings.configs.settings import Settings
from src.core.di.containers import create_bot_container
from src.tg_bot.core.storage import get_storage
from src.tg_bot.domains import commands, routes

settings = Settings()


class TelegramBot:
    def __init__(self):
        self.bot = Bot(token=settings.bot_token.get_secret_value())
        self.storage = get_storage()
        self.dp = Dispatcher(storage=self.storage)
        container = create_bot_container()

        # Подключаем контейнер к диспетчеру
        setup_dishka(container, self.dp)
        self._register_routers()
        self._register_handlers()


    def _register_handlers(self) -> None:
        for command, handler in commands.items():
            self.dp.message.register(handler, Command(command))

    def _register_routers(self) -> None:
        for router in routes:
            self.dp.include_router(router)

    async def on_shutdown(self) -> None:
        await self.storage.close()
        await self.dp.shutdown()

    async def start(self):
        try:
            await self.dp.start_polling(
                self.bot, skip_updates=True, timeout=1, relax=0.1
            )
        except asyncio.CancelledError:
            await self.bot.session.close()
        finally:
            await self.storage.close()
            await self.bot.session.close()
