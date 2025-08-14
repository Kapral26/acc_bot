from aiogram import Bot
from dishka import AsyncContainer, Provider, Scope, make_async_container, provide

from src.tg_bot.bot import TelegramBot
from src.tg_bot.dependencies import ConfigProvider, LoggerProvider
from src.tg_bot.domains.dependencies import (
    ApiAdapterProvider,
    RussianRouletteProvider,
    TrollingPhrasesProvider,
    UserAnalyticsProvider,
    UserBotProvider,
    UserInChatFilterProvider,
)


class BotProvider(Provider):
    @provide(scope=Scope.APP)
    def get_aiogram_bot(self) -> Bot:
        return TelegramBot().bot


def create_taskiq_container() -> AsyncContainer:
    containers = [
        LoggerProvider(),
        ConfigProvider(),
        ApiAdapterProvider(),
        BotProvider(),
        UserInChatFilterProvider(),
        UserBotProvider(),
        RussianRouletteProvider(),
        TrollingPhrasesProvider(),
        UserAnalyticsProvider(),
    ]
    return make_async_container(*containers)
