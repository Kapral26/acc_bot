import logging

from dishka import Provider, Scope, provide


class LoggerProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_logger(self) -> logging.Logger:
        return logging.getLogger("app_logger")
