from dishka import AsyncContainer, \
    make_async_container

from src.app.analytics.bad_phrase.dependencies import BadPhraseProvider
from src.app.analytics.dependencies import AnalyticsProvider
from src.app.dependencies import LoggerProvider, \
    ConfigProvider, \
    DatabaseProvider
from src.app.users.chats.dependencies import ChatsProvider
from src.app.users.dependencies import UserProvider
from src.app.users.roles.dependencies import RolesProvider


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
