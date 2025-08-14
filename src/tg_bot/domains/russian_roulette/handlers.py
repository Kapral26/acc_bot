from aiogram import Bot, F
from aiogram.types import CallbackQuery
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from src.task_manager.tasks import task_collect_analytics
from src.tg_bot.domains.russian_roulette import russian_roulette_router
from src.tg_bot.domains.russian_roulette.keyboards import get_rr_inline_keyboard
from src.tg_bot.domains.russian_roulette.services import RussianRouletteService
from src.tg_bot.domains.user_management.filters import UserInChatFilter


@russian_roulette_router.callback_query(
    F.data == "russia_roulette",
    #   TimeRangeFilter(8, 23),
    UserInChatFilter(),
)
@inject
async def handle_russian_roulette(
    callback: CallbackQuery,
    bot: Bot,
    russian_roulette_service: FromDishka[RussianRouletteService],
):
    await callback.answer("Поиск подходящей фразы....")

    print("перед постановкой задачи")
    try:
        await task_collect_analytics.kiq(callback)
    except Exception as e:
        print(e)
    else:
        print("Поставлена задача")

    try:
        bad_phrase = await russian_roulette_service.start(callback)
    except Exception as e:
        await callback.message.edit_text(f"Проблема при поиске фразы: {e}")
    else:
        await callback.message.edit_text(
            bad_phrase.phrase, reply_markup=await get_rr_inline_keyboard()
        )


@russian_roulette_router.callback_query(
    F.data == "russia_roulette_finish",
    #   TimeRangeFilter(8, 23),
    UserInChatFilter(),
)
@inject
async def handle_russia_roulette_finish(
    callback: CallbackQuery,
    bot: Bot,
):
    await callback.answer("Подсчитываю количество статистики....")
    await callback.message.edit_text(f"@{callback.from_user.username} - Пуська!")
