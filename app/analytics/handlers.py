import uuid
from typing import Annotated

from app.analytics.bad_phrase.schemas import BadPhraseCRUD
from app.analytics.service import AnalyticsService
from app.dependencies import get_analytics_service
from app.settings.broker.kafka import kafka_producer
from app.settings.configs.settings import Settings
from app.users.schemas import UsersCreateSchema
from fastapi import APIRouter, Depends, HTTPException
from starlette import status

router = APIRouter(prefix="/analytics", tags=["Analytics"])
settings = Settings()

# Определим топик для ответов. Можно вынести в настройки.
REPLY_TOPIC = "analytics_replies"

@router.post("/track", status_code=status.HTTP_202_ACCEPTED)
async def track_user_request_async(
        who_send: UsersCreateSchema,
):
    correlation_id = str(uuid.uuid4())

    # Заголовки, чтобы консьюмер знал, куда и как отправить ответ
    headers = [
        ("reply_topic", REPLY_TOPIC.encode("utf-8")),
        ("correlation_id", correlation_id.encode("utf-8"))
    ]

    try:
        # Отправляем событие в основной топик Kafka
        await kafka_producer.send_event(
            topic=settings.kafka_topic,
            event=who_send.model_dump(),
            headers=headers
        )
        return {"message": "Request accepted for processing.", "correlation_id": correlation_id}
    except Exception as e:
        # Обработка случая, если Kafka недоступна
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Could not send message to Kafka: {e}"
        )

# Старый синхронный эндпоинт можно оставить для отладки или удалить
@router.post("/track_sync")
async def create_bad_phrase_request(
        who_send: UsersCreateSchema,
        analytics_service: Annotated[AnalyticsService, Depends(get_analytics_service)],
) -> BadPhraseCRUD:
    """
    (Synchronous) Tracks user request and returns the result directly.
    """
    track_result = await analytics_service.track_user_request(who_send)
    if not track_result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not track request",
        )
    return track_result
