from aiogram import F
from aiogram.types import CallbackQuery
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from src.tg_bot.domains.personal_account.user_analytics import user_analytics_router
from src.tg_bot.domains.personal_account.user_analytics.keyboards import (
    get_user_analytics_inline_keyboard,
)
from src.tg_bot.domains.personal_account.user_analytics.services import (
    UserAnalyticsService,
)


@user_analytics_router.callback_query(F.data == "chat_analytics")
@inject
async def handle_chat_analytics(
        callback: CallbackQuery,
        user_analytics_service: FromDishka[UserAnalyticsService]
):
    await callback.answer("Считаю твою статистику ебаную...")
    message = await user_analytics_service.get_user_statistic_message(callback)
    await callback.message.edit_text(
        message,
        parse_mode="Markdown",
        reply_markup=await get_user_analytics_inline_keyboard(),
    )

