from src.tg_bot.domains.base.handlers import BaseHandlers
from src.tg_bot.domains.russian_roulette import russian_roulette_router
from src.tg_bot.domains.user_management import user_router

commands = {
    "start": BaseHandlers.start_command,
    "help": BaseHandlers.help_command,
}

routes = [russian_roulette_router, user_router]
