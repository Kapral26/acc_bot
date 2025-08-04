import logging
from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import Depends

from src.app.dependencies import get_logger
from src.app.settings.database.database import async_session_factory
from src.app.users.chats.repository import ChatsRepository
from src.app.users.chats.service import ChatsService


async def get_chat_repository() -> ChatsRepository:
    return ChatsRepository(session_factory=async_session_factory)


@inject
def get_chats_service(
    chats_repository: Annotated[ChatsRepository, Depends(get_chat_repository)],
    logger: FromDishka[logging.Logger],
) -> ChatsService:
    return ChatsService(chats_repository=chats_repository, logger=logger)
