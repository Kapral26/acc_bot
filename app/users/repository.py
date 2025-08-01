import logging
from collections.abc import Callable
from dataclasses import dataclass
from typing import TypeVar

from sqlalchemy import and_, func, insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.chats.repository import get_chat_id
from app.users.models import User, UserChats
from app.users.schemas import UsersCreateSchema

T = TypeVar("T")


async def find_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def find_user_by_id(session: AsyncSession, id: int) -> User | None:
    stmt = select(User).where(User.id == id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def insert_new_user(session: AsyncSession, user_data: UsersCreateSchema) -> int:
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


async def get_random_user(session: AsyncSession) -> User | None:
    stmt = select(User).order_by(func.random()).limit(1)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


@dataclass
class UserRepository:
    session_factory: Callable[[T], AsyncSession]
    logger: logging.Logger

    async def create_user(self, user_data: UsersCreateSchema) -> None:
        async with self.session_factory() as session:
            self.logger.info(f"Register new user: {user_data}")
            chat_id = await get_chat_id(session, user_data.chat)
            self.logger.info(f"Chat ID: {chat_id}")

            exist_user = await find_user_by_id(session, user_data.id)
            if not exist_user:
                self.logger.debug("User doesn`t exist. Inserting new user.")
                new_user_id = await insert_new_user(session, user_data)
            else:
                new_user_id = exist_user.id

            await self.bind_chat_to_user(session, new_user_id, chat_id)
            (await self.set_user_base_role(session, new_user_id, chat_id),)

            self.logger.info(
                f"base role was set and bind to chat: {chat_id} for user: {new_user_id}"
            )

            await session.commit()

            self.logger.info(f"User was created successfully. ID: {new_user_id}")

    async def get_users(self) -> list[User]:
        async with self.session_factory() as session:
            query_result = await session.execute(select(User))
            return query_result.scalars().all()

    async def get_user_by_id(self, user_id: int) -> User | None:
        async with self.session_factory() as session:
            user = await find_user_by_id(session, user_id)
            return user

    async def get_user_by_username(self, username: str) -> User | None:
        async with self.session_factory() as session:
            # Сбрасываем кэш SQLAlchemy
            session.expire_all()
            user = await find_user_by_username(session, username)
            return user

    async def bind_chat_to_user(
        self, session: AsyncSession, user_id: int, chat_id: int
    ):
        stmt = insert(UserChats).values(chat_id=chat_id, user_id=user_id)
        try:
            await session.execute(stmt)
        except IntegrityError:
            self.logger.debug("У пользователя уже есть права в данном чате.")
            pass
        except Exception as e:
            self.logger.error(str(e))
            raise
        else:
            await session.commit()

    async def is_user_in_chat(
        self, session: AsyncSession, user_id: int, chat_id: int
    ) -> bool:
        stmt = select(UserChats).where(
            and_(UserChats.user_id == user_id, UserChats.chat_id == chat_id)
        )
        result = await session.execute(stmt)
        return result.scalar_one_or_none() is not None
