from dishka import AsyncContainer, make_async_container

from src.tg_bot.dependencies import ConfigProvider, LoggerProvider
from src.tg_bot.domains.dependencies import (
    ApiAdapterProvider,
    RussianRouletteProvider,
    UserBotProvider,
    UserInChatFilterProvider,
)


def create_bot_container() -> AsyncContainer:
    containers = [
        LoggerProvider(),
        ConfigProvider(),
        ApiAdapterProvider(),
        UserInChatFilterProvider(),
        UserBotProvider(),
        RussianRouletteProvider(),
    ]
    return make_async_container(*containers)
