from collections.abc import Callable
from dataclasses import dataclass
from typing import TypeVar

from sqlalchemy import insert, select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.models import User

T = TypeVar("T")

async def find_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def get_random_user(session: AsyncSession) -> User | None:
    stmt = select(User).order_by(func.random()).limit(1)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

@dataclass
class UserRepository:
    """
    Класс для работы с пользователями в базе данных.

    Атрибуты:
    session_factory (Callable[[T], AsyncSession]): Фабрика асинхронных сессий.

    Методы:
    create_user(self, username: str, password: str) -> UserProfile: Создает нового пользователя.
    get_user(self, user_id: int) -> UserProfile | None: Получает пользователя по идентификатору.
    get_user_by_name(self, username: str) -> UserProfile | None: Получает пользователя по имени.
    """

    session_factory: Callable[[T], AsyncSession]



    async def create_user(
            self,
            username: str,
            first_name: str,
            full_name: str
    ) -> User:
        """
        Асинхронный репозиторий для управления пользователями в базе данных.

        Позволяет создавать новых пользователей, получать список всех пользователей,
        а также искать пользователя по идентификатору или имени. Использует асинхронные
        сессии SQLAlchemy для взаимодействия с таблицей пользователей.
        """
        stmnt = (
            insert(User)
            .values(
                username=username,
                first_name=first_name,
                full_name=full_name,
            )
            .returning(User.id)
        )

        async with self.session_factory() as session:
            query_result = await session.execute(stmnt)
            new_user_id = query_result.scalars().first()
            await session.commit()

        new_user = await self.get_user_by_id(new_user_id)
        return new_user


    async def get_users(self) -> list[User]:
        async with self.session_factory() as session:
            query_result = await session.execute(select(User))
            return query_result.scalars().all()


    async def get_user_by_id(self, user_id: int) -> User | None:
        """
        Получает пользователя по идентификатору.

        Описание:
        - Выполняет запрос на выборку пользователя по идентификатору.
        - Возвращает первого найденного пользователя или None, если пользователь не найден.

        Аргументы:
        - user_id: Идентификатор пользователя.

        Возвращает:
        - Найденного пользователя или None, если пользователь не найден.
        """
        query = select(User).where(User.id == user_id)
        async with self.session_factory() as session:
            query_result = await session.execute(query)
            user = query_result.scalars().first()
            return user

    async def get_user_by_name(self, username: str) -> User | None:
        async with self.session_factory() as session:
            # Сбрасываем кэш SQLAlchemy
            session.expire_all()
            user = await self.find_user_by_username(session, username)
            return user
