from dishka.integrations.taskiq import setup_dishka

from src.task_manager.broker import broker
from src.task_manager.containers import create_taskiq_container

container = create_taskiq_container()
setup_dishka(container, broker=broker)
