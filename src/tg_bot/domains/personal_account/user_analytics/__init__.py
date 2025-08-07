from aiogram import Router

user_analytics_router = Router(name="user_analytics")

from src.tg_bot.domains.personal_account.user_analytics import handlers