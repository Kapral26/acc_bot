from aiogram import Bot, F, types
from aiogram.enums import ChatType
from aiogram.filters import Command
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from src.tg_bot.domains.personal_account import personal_account_router
from src.tg_bot.domains.personal_account.keyboards import (
    get_personal_account_inline_keyboard,
)


@personal_account_router.message(Command("start"), F.chat.type == ChatType.PRIVATE)
async def start_private(message: types.Message, bot: Bot):
    await message.answer(
        "`Да, это личный кабинет бота. Нажми на кнопочку.`",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Основное меню", callback_data="main_menu")]
            ]
        ),
    )


@personal_account_router.callback_query(
    F.data == "main_menu",
)
async def private_actions(callback: CallbackQuery):
    await callback.answer("Жую хуи...")

    message = f"""
    <b>🛠️ ЛИЧНЫЙ КАБИНЕТ v2.0 (BETA)</b>

    <i>▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬</i>
    • 👋 <i>Приветствие</i>: "Шалом @{callback.from_user.username}" (но мы оба знаем, что ты не еврей)
    • ✝️ <i>Статус</i>: Православный (на словах)

    <b>⚙️ ДОСТУПНЫЕ ФУНКЦИИ:</b>
    - 🤡 <i>Фразы</i> (чтобы хоть как-то оправдать твое существование)
    - 📉 <i>Статистика</i> (увидишь, как все забили на тебя хуй)

    <i>▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬</i>
    <code>⚠️ Системное уведомление:
    Твой ID: {callback.from_user.id}
    Местоположение: Не на хую.
    Рекомендация: Иди нахуй</code>
    """

    await callback.message.edit_text(
        message,
        parse_mode="HTML",
        reply_markup=await get_personal_account_inline_keyboard(),
    )
