import asyncio
from asyncio import Semaphore

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramRetryAfter
from aiogram.types import CallbackQuery
from dishka import FromDishka
from dishka.integrations.taskiq import inject

from src.task_manager.worker import broker
from src.tg_bot.domains.russian_roulette.keyboards import get_rr_inline_keyboard
from src.tg_bot.domains.russian_roulette.services import RussianRouletteService

semaphore = Semaphore(2)


@broker.task
@inject(patch_module=True)
async def task_collect_analytics(
    callback: CallbackQuery,
    bot: FromDishka[Bot],
    russian_roulette_service: FromDishka[RussianRouletteService],
):
    async with semaphore:
        try:
            bad_phrase = await russian_roulette_service.start(callback)
        except Exception as e:
            await callback.message.edit_text(
                f"Проблема при поиске фразы: {e}",
                reply_markup=await get_rr_inline_keyboard(),
            ).as_(bot)
        else:
            try:
                await callback.message.edit_text(
                    bad_phrase.phrase, reply_markup=await get_rr_inline_keyboard()
                ).as_(bot)
            except TelegramRetryAfter as e:
                await callback.message.edit_text(
                    f"Ну вот телега все заблокировала на {e.retry_after}"
                ).as_(bot)
                await asyncio.sleep(e.retry_after)
                await callback.message.edit_text(
                    bad_phrase.phrase, reply_markup=await get_rr_inline_keyboard()
                ).as_(bot)
            except TelegramBadRequest as e:
                if "message is not modified" in str(e):
                    pass  # Ничего не меняем — уже актуально
