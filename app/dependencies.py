from typing import Annotated

from fastapi import Depends

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