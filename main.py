import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import all_routers
from tg_bot.bot import TelegramBot

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


app = FastAPI(lifespan=lifespan)

for router in all_routers:
    app.include_router(router)
