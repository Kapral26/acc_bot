import logging
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import TypeVar

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.app.users.chats.repository import get_chat_id
from src.app.users.models import User, UserChats
from src.app.users.schemas import UsersCreateSchema

T = TypeVar("T")


@dataclass
class UserRepository:
    session_factory: Callable[[T], AsyncSession]
    logger: logging.Logger

    @staticmethod
    async def _get_user_by_id(session: AsyncSession, id: int) -> User | None:
        stmt = select(User).options(joinedload(User.chats)).where(User.id == id)
        result = await session.execute(stmt)
        return result.scalars().first()

    @staticmethod
    async def _insert_new_user(
        session: AsyncSession, user_data: UsersCreateSchema
    ) -> int:
        stmnt = (
            insert(User)
            .values(
                id=user_data.id,
                username=user_data.username,
                first_name=user_data.first_name,
                last_name=user_data.last_name,
            )
            .returning(User.id)
        )
        try:
            query_result = await session.execute(stmnt)
        except Exception as e:
            await session.rollback()
            raise

        new_user_id = query_result.scalars().first()
        return new_user_id

    async def get_random_user(self, chat_id: int) -> User | None:
        async with self.session_factory() as session:
            stmt = (
                select(User)
                .join(UserChats, User.id == UserChats.user_id)
                .where(UserChats.chat_id == chat_id)
            )
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            return user

    async def create_user(self, user_data: UsersCreateSchema) -> None:
        async with self.session_factory() as session:
            self.logger.info(f"Register new user: {user_data}")
            chat_id = await get_chat_id(session, user_data.chat)
            self.logger.info(f"Chat ID: {chat_id}")

            exist_user = await self._get_user_by_id(session, user_data.id)
            if not exist_user:
                self.logger.debug(
                    "User doesn`t exist into this chat. Inserting new user."
                )
                new_user_id = await self._insert_new_user(session, user_data)
            else:
                new_user_id = exist_user.id

            await self.bind_chat_to_user(session, new_user_id, chat_id)

            await session.commit()

            self.logger.info(f"User was created successfully. ID: {new_user_id}")

    async def get_users(self) -> Sequence[User]:
        async with self.session_factory() as session:
            query_result = await session.execute(
                select(User).options(joinedload(User.chats))
            )
            return query_result.scalars().all()

    async def get_user_by_id(self, user_id: int) -> User | None:
        async with self.session_factory() as session:
            user = await self._get_user_by_id(session, user_id)
            return user

    async def get_user_by_username(self, username: str) -> User | None:
        async with self.session_factory() as session:
            # Сбрасываем кэш SQLAlchemy
            session.expire_all()
            stmt = (
                select(User)
                .options(joinedload(User.chats))
                .where(User.username == username)
            )
            result = await session.execute(stmt)
            return result.scalars().first()

    async def bind_chat_to_user(
        self, session: AsyncSession, user_id: int, chat_id: int
    ):
        stmt = insert(UserChats).values(chat_id=chat_id, user_id=user_id)
        try:
            await session.execute(stmt)
        except Exception as e:
            self.logger.exception(str(e))
            raise
        else:
            await session.commit()
