from dataclasses import dataclass

from aiogram import types

from tg_bot.domains.russian_roulette.repository import RussianRouletteRepository
from tg_bot.domains.russian_roulette.schemas import BadPhraseMessage
from tg_bot.domains.user_management.services import UserBotService


@dataclass
class RussianRouletteService:
    russian_roulette_repository: RussianRouletteRepository
    user_bot_service: UserBotService

    async def start(self, message: types.Message) -> BadPhraseMessage:
        user_who_sand = await self.user_bot_service.extract_user_data(message)
        bad_phrase = await self.russian_roulette_repository.start(user_who_sand)
        return bad_phrase
