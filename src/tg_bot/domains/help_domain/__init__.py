from aiogram import Router

help_router = Router(name="help_router")

from src.tg_bot.domains.help_domain import handlers