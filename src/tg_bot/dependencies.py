import logging

from dishka import Provider, Scope, provide
from src.tg_bot.core.settings.configs.settings import Settings


class LoggerProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_logger(self) -> logging.Logger:
        return logging.getLogger("bot_logger")


class ConfigProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_config(self) -> Settings:
        return Settings()
