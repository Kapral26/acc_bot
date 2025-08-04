from dataclasses import dataclass

from aiogram import types

from src.app.users.schemas import UsersCreateSchema
from src.tg_bot.domains.russian_roulette.repository import RussianRouletteRepository
from src.tg_bot.domains.russian_roulette.schemas import BadPhraseMessage
from src.tg_bot.domains.user_management.services import UserBotService, extract_user_data


@dataclass
class RussianRouletteService:
    russian_roulette_repository: RussianRouletteRepository
    user_bot_service: UserBotService

    @extract_user_data
    async def start(
        self, message: types.Message, user_data: UsersCreateSchema
    ) -> BadPhraseMessage:
        user_who_sand = user_data
        bad_phrase = await self.russian_roulette_repository.start(user_who_sand)
        return bad_phrase
