from tg_bot.domains.api_adapter.service import APIAdapter
from tg_bot.domains.russian_roulette.repository import RussianRouletteRepository
from tg_bot.domains.russian_roulette.services import RussianRouletteService
from tg_bot.domains.user_management.repository import UserBotRepository
from tg_bot.domains.user_management.services import UserBotService

api_adapter = APIAdapter()
user_bot_repository = UserBotRepository(api_adapter=api_adapter)
user_bot_service = UserBotService(user_bot_repository=user_bot_repository)
russian_roulette_repository = RussianRouletteRepository(api_adapter=api_adapter)
russian_roulette_service = RussianRouletteService(
    russian_roulette_repository=russian_roulette_repository,
    user_bot_service=user_bot_service,
)

user_info_repository = UserInfoRepository(user_bot_service=user_bot_service)
user_info_service = UserInfoService(user_info_repository=user_info_repository)
