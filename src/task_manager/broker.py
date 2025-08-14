# src/task_manager/broker.py
from taskiq_aio_pika import AioPikaBroker

from src.task_manager.settings import TaskIqSettings

settings = TaskIqSettings()

broker = AioPikaBroker(
    url=settings.url,
    queue_name=settings.queue_name,
)
