import logging

from dishka import FromDishka, Provider, Scope, provide

from src.tg_bot.core.api_adapter.service import APIAdapter
from src.tg_bot.domains.personal_account.trolling_phrases.repository import (
    TrollingPhrasesRepository,
)
from src.tg_bot.domains.personal_account.trolling_phrases.services import (
    TrollingPhrasesService,
)
from src.tg_bot.domains.personal_account.user_analytics.repository import (
    UserAnalyticsRepository,
)
from src.tg_bot.domains.personal_account.user_analytics.services import (
    UserAnalyticsService,
)
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
        logger: FromDishka[logging.Logger],
    ) -> UserBotService:
        return UserBotService(user_bot_repository=user_bot_repository, logger=logger)


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


class TrollingPhrasesProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_trolling_phrases_repository(
        self, api_adapter: FromDishka[APIAdapter]
    ) -> TrollingPhrasesRepository:
        return TrollingPhrasesRepository(api_adapter=api_adapter)

    @provide(scope=Scope.REQUEST)
    async def get_trolling_phrases_service(
        self,
        repository: FromDishka[TrollingPhrasesRepository],
    ) -> TrollingPhrasesService:
        return TrollingPhrasesService(trolling_phrases_repository=repository)


class UserAnalyticsProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_trolling_phrases_repository(
        self, api_adapter: FromDishka[APIAdapter]
    ) -> UserAnalyticsRepository:
        return UserAnalyticsRepository(api_adapter=api_adapter)

    @provide(scope=Scope.REQUEST)
    async def get_trolling_phrases_service(
        self,
        repository: FromDishka[UserAnalyticsRepository],
    ) -> UserAnalyticsService:
        return UserAnalyticsService(user_analytics_repository=repository)


class UserInChatFilterProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_user_in_chat_filter(
        self,
    ) -> UserInChatFilter:
        return UserInChatFilter()
