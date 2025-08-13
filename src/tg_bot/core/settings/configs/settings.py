import logging
from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.tg_bot.core.settings.configs.logger import setup_file_logger

dotenv_path = Path(__file__).parent.parent.parent.parent.absolute() / ".env"


class Settings(BaseSettings):
    """Класс настроек."""

    debug: bool = Field(..., alias="DEBUG")

    kafka_bootstrap_servers: str = Field(..., alias="KAFKA_BOOTSTRAP_SERVERS")
    kafka_topic: str = Field(..., alias="KAFKA_TOPIC")
    kafka_port: str = Field(..., alias="KAFKA_PORT")
    kafka_consumer_group: str = Field(..., alias="KAFKA_CONSUMER_GROUP")

    bot_token: SecretStr = Field(..., alias="BOT_TOKEN")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        setup_file_logger(
            log_file="bot.log",
            logger_name="bot_logger",
            log_level=logging.INFO if not self.debug else logging.DEBUG,
        )

    @property
    def kafka_servers_dsn(self) -> str:
        return f"{self.kafka_bootstrap_servers}:{self.kafka_port}"

    model_config = SettingsConfigDict(env_file=dotenv_path, env_file_encoding="utf-8")


if __name__ == "__main__":
    settings = Settings()
    a = 1
