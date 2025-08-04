from src.tg_bot.domains.base.handlers import BaseHandlers
from src.tg_bot.domains.russian_roulette import router as russian_roulette_router
from src.tg_bot.domains.user_management.handlers import UserHandlers

commands = {
    "start": BaseHandlers.start_command,
    "help": BaseHandlers.help_command,
    "reg_user": UserHandlers.reg_user,
}

routes = [russian_roulette_router]
