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


async def get_phrases_keyboards(page: int, total_pages: int):
    # Создаем клавиатуру с пагинацией
    builder = InlineKeyboardBuilder()
    # Кнопки пагинации
    if page > 1:
        builder.button(text="⬅️ Назад", callback_data=f"phrases_page_{page - 1}")
    if page < total_pages:
        builder.button(text="Вперед ➡️", callback_data=f"phrases_page_{page + 1}")
    # Кнопка возврата
    builder.button(text="🔙 Назад", callback_data="trolling_phrases")
    builder.adjust(2)  # Группируем кнопки пагинации
    return builder.as_markup()
