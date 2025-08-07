from aiogram import Router

trolling_phrases_router = Router(name="trolling_phrases")

from src.tg_bot.domains.personal_account.trolling_phrases import handlers