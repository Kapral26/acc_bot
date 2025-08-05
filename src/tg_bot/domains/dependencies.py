from dishka import FromDishka, Provider, Scope, provide

from src.tg_bot.domains.api_adapter.service import APIAdapter
from src.tg_bot.domains.russian_roulette.repository import RussianRouletteRepository
from src.tg_bot.domains.russian_roulette.services import RussianRouletteService
from src.tg_bot.domains.user_management.filters import UserInChatFilter
from src.tg_bot.domains.user_management.repository import UserBotRepository
from src.tg_bot.domains.user_management.services import UserBotService


class ApiAdapterProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_api_adatpter(self) -> APIAdapter:
        return APIAdapter()


class UserBotProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_user_bot_repository(
        self,
        api_adapter: FromDishka[APIAdapter],
    ) -> UserBotRepository:
        return UserBotRepository(api_adapter=api_adapter)

    @provide(scope=Scope.REQUEST)
    async def get_user_bot_service(
        self,
        user_bot_repository: FromDishka[UserBotRepository],
    ) -> UserBotService:
        return UserBotService(user_bot_repository=user_bot_repository)


class RussianRouletteProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_russian_roulette_repository(
        self, api_adapter: FromDishka[APIAdapter]
    ) -> RussianRouletteRepository:
        return RussianRouletteRepository(api_adapter=api_adapter)

    @provide(scope=Scope.REQUEST)
    async def get_russian_roulette_service(
        self,
        repository: FromDishka[RussianRouletteRepository],
    ) -> RussianRouletteService:
        return RussianRouletteService(russian_roulette_repository=repository)


class UserInChatFilterProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_user_in_chat_filter(
        self,
    ) -> UserInChatFilter:
        return UserInChatFilter()
