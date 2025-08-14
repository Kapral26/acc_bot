
from pydantic import Field
from pydantic_settings import BaseSettings


class TaskIqSettings(BaseSettings):
    url: str = Field("amqp://admin:admin@localhost:5672/")
    queue_name: str = Field("taskiq_akk_bot")
