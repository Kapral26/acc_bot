

from tg_bot.domains.api_adapter.service import APIAdapter
from tg_bot.domains.user_management.repository import UserBotRepository
from tg_bot.domains.user_management.services import UserBotService

api_adapter = APIAdapter()
user_bot_repository = UserBotRepository(api_adapter=api_adapter)
user_bot_service = UserBotService(user_bot_repository=user_bot_repository)
