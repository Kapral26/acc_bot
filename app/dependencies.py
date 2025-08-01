import logging
from typing import Annotated

from app.analytics.bad_phrase.repository import BadPhraseRepository
from app.analytics.bad_phrase.service import BadPhraseService
from app.analytics.repository import AnalyticsRepository
from app.analytics.service import AnalyticsService
from app.settings.database.database import async_session_factory
from app.users.chats.repository import ChatsRepository
from app.users.chats.service import ChatsService
from app.users.repository import UserRepository
from app.users.roles.repository import RolesRepository
from app.users.roles.service import RolesService
from app.users.service import UserService
from fastapi import Depends


def get_logger() -> logging.Logger:
    return logging.getLogger("app_logger")

async def get_roles_repository() -> RolesRepository:
    return RolesRepository(session_factory=async_session_factory)

def get_roles_service(
        roles_repository: Annotated[RolesRepository, Depends(get_roles_repository)],
) -> RolesService:
    return RolesService(roles_repository=roles_repository)

async def get_analytics_repository() -> AnalyticsRepository:
    return AnalyticsRepository(session_factory=async_session_factory)


def get_analytics_service(
        analytics_repository: Annotated[AnalyticsRepository, Depends(get_analytics_repository)],
) -> AnalyticsService:
    return AnalyticsService(analytics_repository=analytics_repository)

async def get_bad_phrase_repository() -> BadPhraseRepository:
    return BadPhraseRepository(session_factory=async_session_factory)

def get_bad_phrase_service(
        bad_phrase_repository: Annotated[BadPhraseRepository, Depends(get_bad_phrase_repository)],
) -> BadPhraseService:
    return BadPhraseService(bad_phrase_repository=bad_phrase_repository)

async def get_chat_repository() -> ChatsRepository:
    return ChatsRepository(session_factory=async_session_factory)

def get_chats_service(
        chats_repository: Annotated[ChatsRepository, Depends(get_chat_repository)],
) -> ChatsService:
    return ChatsService(chats_repository=chats_repository)

async def get_user_repository(
        logger: logging.Logger = Depends(get_logger)
) -> UserRepository:

    return UserRepository(
        session_factory=async_session_factory,
        logger = logger,
    )

def get_user_service(
        user_repository: Annotated[UserRepository, Depends(get_user_repository)],
        chat_repository: Annotated[ChatsRepository, Depends(get_chat_repository)],
        role_repository: Annotated[RolesRepository, Depends(get_roles_repository)],
) -> UserService:
    return UserService(
        user_repository=user_repository,
        chat_repository=chat_repository,
        role_repository=role_repository
    )
