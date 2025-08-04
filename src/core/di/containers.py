from dishka import AsyncContainer, make_async_container

from src.app.analytics.bad_phrase.dependencies import BadPhraseProvider
from src.app.analytics.dependencies import AnalyticsProvider
from src.app.dependencies import ConfigProvider, DatabaseProvider, LoggerProvider
from src.app.users.chats.dependencies import ChatsProvider
from src.app.users.dependencies import UserProvider
from src.app.users.roles.dependencies import RolesProvider
from src.tg_bot.domains.dependencies import (
    ApiAdapterProvider,
    RussianRouletteProvider,
    UserBotProvider,
    UserInChatFilterProvider,
)


def create_api_container() -> AsyncContainer:
    containers = [
        LoggerProvider(),
        ConfigProvider(),
        DatabaseProvider(),
        BadPhraseProvider(),
        ChatsProvider(),
        AnalyticsProvider(),
        RolesProvider(),
        UserProvider(),
    ]

    return make_async_container(*containers)

def create_bot_container() -> AsyncContainer:
    containers = [
        ApiAdapterProvider(),
        UserInChatFilterProvider(),
        UserBotProvider(),
        RussianRouletteProvider(),
    ]
    return make_async_container(*containers)