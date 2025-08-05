import logging
from datetime import UTC, datetime, timedelta
from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.app.settings.configs.logger import setup_file_logger

dotenv_path = Path(__file__).parent.parent.parent.parent.absolute() / ".dev.env"


class Settings(BaseSettings):
    """Класс настроек."""

    # Желательно вместо str использовать SecretStr
    # для конфиденциальных данных, например, токена бота

    postgres_user: str = Field(
        ..., alias="POSTGRES_USER"
    )  # Имя пользователя базы данных
    postgres_password: SecretStr = Field(..., alias="POSTGRES_PASSWORD")
    # Пароль пользователя, хранится как SecretStr для безопасности
    postgres_db: str = Field(..., alias="POSTGRES_DB")  # Название базы данных
    postgres_host: str = Field(..., alias="POSTGRES_HOST")  # Хост-сервера базы данных
    postgres_port: int = Field(..., alias="POSTGRES_PORT")  # Порт сервера базы данных
    debug: bool = Field(..., alias="DEBUG")

    redis_host: str = Field(..., alias="REDIS_HOST")
    redis_port: int = Field(..., alias="REDIS_PORT")
    redis_db: int = Field(..., alias="REDIS_DB")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        setup_file_logger(log_level=logging.INFO if not self.debug else logging.DEBUG)

    @property
    def async_database_dsn(self) -> str:
        """Возвращает объект URL для подключения к PostgreSQL с использованием sqlalchemy и драйвера psycopg2."""
        return (
            f"postgresql+asyncpg://{self.postgres_user}:"
            f"{self.postgres_password.get_secret_value()}@"
            f"{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def jwt_expires(self) -> float:
        """
        Возвращает время истечения срока действия JWT-токена.

        Возвращает:
            float: Время истечения срока действия JWT-токена в формате Unix timestamp.
        """
        return (datetime.now(UTC) + timedelta(days=self.jwt_token_lifetime)).timestamp()

    model_config = SettingsConfigDict(env_file=dotenv_path, env_file_encoding="utf-8")


if __name__ == "__main__":
    settings = Settings()
    a = 1
