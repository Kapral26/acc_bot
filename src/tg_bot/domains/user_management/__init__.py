from aiogram import Router

user_router = Router(name="user_router")

from src.tg_bot.domains.user_management import handlers