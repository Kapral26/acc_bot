from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dishka.integrations.aiogram import inject


@inject
async def get_personal_account_inline_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=f"Раздел с фразами. 📝",
            callback_data="trolling_phrases",
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=f"Аналитика по чатам. 📊",
            callback_data="chat_analytics",
        )
    )

    return builder.as_markup()
