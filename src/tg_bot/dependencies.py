import logging

from dishka import Provider, Scope, provide

from src.tg_bot.core.settings.configs.settings import Settings


class LoggerProvider(Provider):
    """
    Провайдер для получения экземпляра логгера.

    Этот провайдер используется в контейнере зависимостей (dependency injection),
    чтобы предоставлять общий экземпляр логгера на уровне приложения.
    """

    @provide(scope=Scope.APP)
    async def get_logger(self) -> logging.Logger:
        """
        Создаёт и возвращает логгер с именем 'bot_logger'.

        Returns:
            logging.Logger: Экземпляр логгера, настроенного для использования в боте.

        """
        return logging.getLogger("bot_logger")


class ConfigProvider(Provider):
    """
    Провайдер для загрузки конфигурации приложения.

    Загружает настройки из файла или окружения с использованием класса `Settings`.
    """

    @provide(scope=Scope.APP)
    async def get_config(self) -> Settings:
        """
        Возвращает объект настроек приложения.

        Returns:
            Settings: Объект, содержащий конфигурационные данные.

        """
        return Settings()
