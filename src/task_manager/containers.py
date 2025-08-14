from dishka import AsyncContainer, make_async_container

from src.tg_bot.dependencies import ConfigProvider, LoggerProvider
from src.tg_bot.domains.dependencies import (
    ApiAdapterProvider,
    RussianRouletteProvider,
    TrollingPhrasesProvider,
    UserAnalyticsProvider,
    UserBotProvider,
    UserInChatFilterProvider,
)


def create_taskiq_container() -> AsyncContainer:
    containers = [
        LoggerProvider(),
        ConfigProvider(),
        ApiAdapterProvider(),
        UserInChatFilterProvider(),
        UserBotProvider(),
        RussianRouletteProvider(),
        TrollingPhrasesProvider(),
        UserAnalyticsProvider(),
    ]
    return make_async_container(*containers)
