from typing import Annotated

from fastapi import Depends

from app.analytics.bad_phrase.repository import BadPhraseRepository
from app.analytics.bad_phrase.service import BadPhraseService
from app.analytics.repository import AnalyticsRepository
from app.analytics.service import AnalyticsService
from app.roles.repository import RolesRepository
from app.roles.service import RolesService
from app.settings.database.database import async_session_factory
from app.users.repository import UserRepository
from app.users.service import UserService


async def get_user_repository() -> UserRepository:
    """
    Функция для получения экземпляра класса UserRepository.

    Возвращает:
    UserRepository: Экземпляр класса UserRepository, который используется для работы с пользователями в базе данных.

    Примечание:
    Эта функция используется для получения экземпляра класса UserRepository,
    который используется для работы с пользователями в базе данных.
    Экземпляр класса UserRepository создается с использованием фабрики асинхронных сессий async_session_factory.
    """
    return UserRepository(session_factory=async_session_factory)

def get_user_service(
        user_repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> UserService:
    """
    Функция для получения экземпляра UserService.

    :param user_repository: Репозиторий пользователей.
    :param auth_service: Сервис аутентификации.
    :return: Экземпляр UserService.
    """
    return UserService(user_repository=user_repository)

async def get_roles_repository() -> RolesRepository:
    return RolesRepository(session_factory=async_session_factory)

def get_roles_service(
        roles_repository: Annotated[RolesRepository, Depends(get_roles_repository)],
) -> RolesService:
    return RolesService(roles_repository=roles_repository)


async def get_analytics_repository() -> RolesRepository:
    return AnalyticsRepository(session_factory=async_session_factory)

def get_analytics_service(
        analytics_repository: Annotated[RolesRepository, Depends(get_analytics_repository)],
) -> AnalyticsService:
    return AnalyticsService(analytics_repository=analytics_repository)

async def get_bad_phrase_repository() -> BadPhraseRepository:
    return BadPhraseRepository(session_factory=async_session_factory)

def get_bad_phrase_service(
        bad_phrase_repository: Annotated[BadPhraseRepository, Depends(get_bad_phrase_repository)],
) -> BadPhraseService:
    return BadPhraseService(bad_phrase_repository=bad_phrase_repository)
