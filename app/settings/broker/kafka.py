import asyncio
import json
import logging
from typing import List, Optional, Tuple

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from fastapi import FastAPI

from app.analytics.bad_phrase.schemas import BadPhraseCRUD

# Импортируем зависимости, необходимые для обработки сообщений
from app.analytics.dependencies import get_analytics_service
from app.settings.configs.settings import Settings
from app.users.schemas import UsersCreateSchema

settings = Settings()
logger = logging.getLogger(__name__)


class KafkaProducer:
    def __init__(self, bootstrap_servers: str = settings.kafka_bootstrap_servers):
        self.bootstrap_servers = bootstrap_servers
        self.producer: Optional[AIOKafkaProducer] = None

    async def start(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
        await self.producer.start()
        logger.info("Kafka producer started.")

    async def stop(self):
        if self.producer:
            await self.producer.stop()
            logger.info("Kafka producer stopped.")

    async def send_event(
        self, topic: str, event: dict, headers: Optional[List[Tuple[str, bytes]]] = None
    ):
        if not self.producer:
            raise RuntimeError("Kafka producer not started")
        await self.producer.send_and_wait(topic, event, headers=headers)


class KafkaConsumer:
    def __init__(
        self,
        bootstrap_servers: str = settings.kafka_bootstrap_servers,
        topic: str = settings.kafka_topic,
        group_id: str = "analytics-group",
    ):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.group_id = group_id
        self.consumer: Optional[AIOKafkaConsumer] = None
        self._consumer_task: Optional[asyncio.Task] = None

    async def start(self):
        self.consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        )
        await self.consumer.start()
        self._consumer_task = asyncio.create_task(self.consume())
        logger.info(f"Kafka consumer started for topic '{self.topic}'.")

    async def stop(self):
        if self.consumer:
            await self.consumer.stop()
        if self._consumer_task:
            self._consumer_task.cancel()
        logger.info("Kafka consumer stopped.")

    async def consume(self):
        try:
            async for msg in self.consumer:
                logger.info(f"Consumed message from topic '{msg.topic}': {msg.value}")
                try:
                    # Для каждого сообщения получаем новый экземпляр сервиса
                    # Это гарантирует, что у нас будет свежая сессия БД и другие ресурсы
                    async for analytics_service in get_analytics_service():
                        who_send = UsersCreateSchema(**msg.value)
                        track_result: BadPhraseCRUD = await analytics_service.track_user_request(who_send)

                        # Проверяем, нужно ли отправлять ответ
                        reply_topic_header = next((h for h in msg.headers if h[0] == 'reply_topic'), None)
                        correlation_id_header = next((h for h in msg.headers if h[0] == 'correlation_id'), None)

                        if reply_topic_header and correlation_id_header:
                            reply_topic = reply_topic_header[1].decode('utf-8')
                            correlation_id = correlation_id_header[1] # Keep as bytes

                            reply_headers = [('correlation_id', correlation_id)]
                            reply_event = track_result.model_dump()

                            logger.info(f"Sending reply to topic '{reply_topic}' with correlation_id")
                            await kafka_producer.send_event(
                                topic=reply_topic,
                                event=reply_event,
                                headers=reply_headers
                            )
                except Exception as e:
                    logger.error(f"Error processing message: {e}", exc_info=True)

        except asyncio.CancelledError:
            logger.info("Consumer task cancelled.")
        finally:
            logger.info("Stopping consumer loop.")


kafka_producer = KafkaProducer()
kafka_consumer = KafkaConsumer()


def register_kafka_events(app: FastAPI):
    @app.on_event("startup")
    async def startup_event():
        await kafka_producer.start()
        await kafka_consumer.start()

    @app.on_event("shutdown")
    async def shutdown_event():
        await kafka_producer.stop()
        await kafka_consumer.stop()