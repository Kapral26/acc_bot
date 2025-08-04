import logging
from typing import Annotated

from fastapi import Depends

from src.app.dependencies import get_logger
from src.app.settings.database.database import async_session_factory
from src.app.users.chats.dependencies import get_chats_service
from src.app.users.chats.service import ChatsService
from src.app.users.repository import UserRepository
from src.app.users.roles.dependencies import get_roles_service
from src.app.users.roles.service import RolesService
from src.app.users.service import UserService


async def get_user_repository(
    logger: Annotated[logging.Logger, Depends(get_logger)],
) -> UserRepository:
    return UserRepository(
        session_factory=async_session_factory,
        logger=logger,
    )


def get_user_service(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    chat_service: Annotated[ChatsService, Depends(get_chats_service)],
    role_service: Annotated[RolesService, Depends(get_roles_service)],
) -> UserService:
    return UserService(
        user_repository=user_repository,
        chat_service=chat_service,
        role_service=role_service,
    )
