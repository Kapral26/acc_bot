from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dishka.integrations.aiogram import inject


@inject
async def get_trolling_phrases_inline_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=f"Просмотр архива 📝",
            callback_data="all_phrases",
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=f"Добавление новой",
            callback_data="add_phrases",
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=f"Удаление",
            callback_data="delete_phrases",
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=f"Назад",
            callback_data="main_menu",
        )
    )

    return builder.as_markup()
