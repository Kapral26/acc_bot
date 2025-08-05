from aiogram import Bot, F, types
from aiogram.filters import Command
from aiogram.types import CallbackQuery
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from src.tg_bot.domains.start_domain.keyboards import get_start_inline_keyboard
from src.tg_bot.domains.user_management import user_router
from src.tg_bot.domains.user_management.services import UserBotService


@user_router.message(Command("reg_user"))
@inject
async def reg_user(
    message: types.Message, user_bot_service: FromDishka[UserBotService]
) -> None:
    try:
        register_suer_result = await user_bot_service.register_user(message)
    except Exception as e:
        await message.answer(f"Проблема при добавлении пользователя: {e}")
    else:
        await message.answer(register_suer_result)


@user_router.callback_query(F.data == "register")
@inject
async def handle_register(
    callback: CallbackQuery, bot: Bot, user_bot_service: FromDishka[UserBotService]
):
    await callback.answer("Регистрация...")

    user = await user_bot_service.is_user_in_chat(callback)

    if user.in_chat:
        await callback.message.edit_text(
            "Ты шо дурак? Ты уже зарегистрирован!",
            reply_markup=await get_start_inline_keyboard(bot, user.in_chat),
        )
    try:
        register_suer_result = await user_bot_service.register_user(callback)
    except Exception as e:
        await callback.message.edit_text(f"Проблема при добавлении пользователя: {e}")
    else:
        await callback.message.edit_text(register_suer_result)
