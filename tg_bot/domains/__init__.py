from tg_bot.domains.base.handlers import BaseHandlers
from tg_bot.domains.russian_roulette.handlers import russian_roulette
from tg_bot.domains.user_management.handlers import UserHandlers

commands = {
    "start": BaseHandlers.start_command,
    "help": BaseHandlers.help_command,
    "reg_user": UserHandlers.reg_user,
    "russian_roulette": russian_roulette,
}
