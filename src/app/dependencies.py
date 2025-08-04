import logging

from dishka import Provider, provide, Scope


def get_logger() -> logging.Logger:
    return


class LoggerProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_logger(self) -> logging.Logger:
        return logging.getLogger("app_logger")
