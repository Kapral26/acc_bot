from aiogram import Router

personal_account_router = Router(name="user_router")

from src.tg_bot.domains.personal_account import handlers