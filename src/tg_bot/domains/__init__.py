from src.tg_bot.domains.help_domain import help_router
from src.tg_bot.domains.personal_account import personal_account_router
from src.tg_bot.domains.personal_account.trolling_phrases import trolling_phrases_router
from src.tg_bot.domains.personal_account.user_analytics import user_analytics_router
from src.tg_bot.domains.russian_roulette import russian_roulette_router
from src.tg_bot.domains.start_domain import start_router
from src.tg_bot.domains.user_management import user_router

routes = [
    russian_roulette_router,
    user_router,
    start_router,
    help_router,
    personal_account_router,
    trolling_phrases_router,
    user_analytics_router,
]
