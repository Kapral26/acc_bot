from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dishka.integrations.aiogram import inject


@inject
async def get_rr_inline_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Найти жертву 🖕🏿", callback_data="russia_roulette"),
    )
    builder.row(
        InlineKeyboardButton(
            text="Завершить игру 🫡", callback_data="russia_roulette_finish"
        ),
    )

    return builder.as_markup()
