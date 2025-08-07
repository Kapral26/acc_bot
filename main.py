import asyncio
from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from src.app import all_routers
from src.app.settings.di.containers import create_api_container
from src.tg_bot.bot import TelegramBot

bot_instance = None  # Глобальная переменная для хранения экземпляра бота


@asynccontextmanager
async def lifespan(app: FastAPI):
    global bot_instance

    # Создаём экземпляр бота
    bot_instance = TelegramBot()

    # Запускаем бота в фоне без await
    bot_task = asyncio.create_task(bot_instance.start())

    yield  # FastAPI работает здесь

    # Корректно останавливаем бота
    bot_task.cancel()
    try:
        await bot_task
    except asyncio.CancelledError:
        pass
    finally:
        await bot_instance.on_shutdown()


container = create_api_container()
app = FastAPI(lifespan=lifespan)
setup_dishka(container, app)

for router in all_routers:
    app.include_router(router)
