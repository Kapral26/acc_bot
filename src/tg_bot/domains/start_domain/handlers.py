from aiogram import Bot, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.tg_bot.domains.start_domain import start_router
from src.tg_bot.domains.start_domain.keyboards import get_start_inline_keyboard
from src.tg_bot.domains.user_management.filters import UserInChatFilter


@start_router.message(Command("start"))
async def start_command(
    message: types.Message,
    bot: Bot,
) -> None:
    """Обработчик команды /start."""
    is_registered = False
    bot = await bot.get_me()
    kb = await get_start_inline_keyboard(bot.username, is_registered)
    await message.answer(
        "Привет! Я бот с базовыми командами. Используй /help для списка команд.",
        reply_markup=kb,
    )


@start_router.message(Command("lk"), UserInChatFilter())
async def start_command(message: types.Message, bot: Bot) -> None:
    """Обработчик команды /start."""
    bot_info = await bot.get_me()
    bot_username = bot_info.username

    if message.chat.type == "private":
        # Личный чат - клавиатура ReplyKeyboardMarkup
        reply_keyboard = types.ReplyKeyboardMarkup(
            keyboard=[
                [
                    types.KeyboardButton(text="1"),
                    types.KeyboardButton(text="2"),
                    types.KeyboardButton(text="3"),
                ]
            ],
            resize_keyboard=True,
        )
        await message.answer("Выберите опцию:", reply_markup=reply_keyboard)
    else:
        # Публичный чат - inline-кнопка для перехода в личный чат
        inline_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Личный кабинет",
                        url=f"https://t.me/{bot_username}?start",
                    )
                ]
            ]
        )
        await message.answer("Перейдите в личный чат:", reply_markup=inline_keyboard)
