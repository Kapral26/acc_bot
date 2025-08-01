import logging
from typing import Annotated

from fastapi import Depends

from app.dependencies import get_logger
from app.settings.database.database import async_session_factory
from app.users.chats.repository import ChatsRepository
from app.users.chats.service import ChatsService


async def get_chat_repository() -> ChatsRepository:
    return ChatsRepository(session_factory=async_session_factory)


def get_chats_service(
    chats_repository: Annotated[ChatsRepository, Depends(get_chat_repository)],
    logger: Annotated[logging.Logger, Depends(get_logger)],
) -> ChatsService:
    return ChatsService(chats_repository=chats_repository, logger=logger)
