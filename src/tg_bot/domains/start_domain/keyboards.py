"""
- [ ] Зарегистрироваться - Если пользователь зарегистрирован - добавить иконку галочки
- [ ] Личный кабинет -> Открывает личный чат бота
- [ ] Играть в рулетку -> Появляется клавиатура для игры
"""

from aiogram import F
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.tg_bot.domains.user_management import user_router


async def get_start_inline_keyboard(
    bot_username: str, is_registered: bool
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    # Личный кабинет — ведёт в чат бота
    builder.row(
        InlineKeyboardButton(
            text=f"Личный кабинет {'✅' if is_registered else ''}",
            url=f"https://t.me/{bot_username}?start",
        )
    )

    # Регистрация — триггерит callback
    builder.row(
        InlineKeyboardButton(text="Зарегистрироваться", callback_data="register")
    )

    return builder.as_markup()


# --- Обработчик нажатия на Inline кнопку ---
@user_router.callback_query(F.data == "register")
async def handle_register(callback: CallbackQuery):
    await callback.answer("Вы зарегистрированы!")  # Ответ пользователю
    await callback.message.edit_text("Регистрация успешна!✅")  # Изменить сообщение
