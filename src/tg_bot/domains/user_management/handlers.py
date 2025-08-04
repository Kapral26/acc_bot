from aiogram import types
from aiogram.filters import Command
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from src.tg_bot.domains.user_management import user_router
from src.tg_bot.domains.user_management.services import UserBotService


@user_router.message(Command("reg_user"))
@inject
async def reg_user(
        message: types.Message,
        user_bot_service: FromDishka[UserBotService]
) -> None:
    try:
        register_suer_result = await user_bot_service.register_user(message)
    except Exception as e:
        await message.answer(f"Проблема при добавлении пользователя: {e}")
    else:
        await message.answer(register_suer_result)