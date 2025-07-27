import logging
from collections.abc import Callable
from dataclasses import dataclass
from typing import TypeVar

from app.users.chats.repository import get_chat_id
from app.users.exceptions import (
    UserRoleHasAlreadyBeenEstablishedException,
    UserRoleNotFount,
    UserWasExits,
)
from app.users.models import User, UserRoles
from app.users.roles.repository import find_role_by_name
from app.users.schemas import UsersCreateSchema
from sqlalchemy import and_, func, insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

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
    session_factory: Callable[[T], AsyncSession]
    logger: logging.Logger
    async def create_user(
            self,
            user_data: UsersCreateSchema
    ) -> User:
        async with self.session_factory() as session:
            self.logger.info(f"Register new user: {user_data}")
            chat_id = await get_chat_id(
                session,
                user_data.chat
            )
            self.logger.info(f"Chat ID: {chat_id}")

            stmnt = (
                insert(User)
                .values(
                    username=user_data.username,
                    first_name=user_data.first_name,
                    last_name=user_data.last_name,
                    chat_id=chat_id,
                )
                .returning(User.id)
            )

            try:
                query_result = await session.execute(stmnt)
            except IntegrityError:
                await session.rollback()
                self.logger.error(UserWasExits.detail)
                raise UserWasExits
            except Exception as e:
                self.logger.error(str(e))
                raise

            new_user_id = query_result.scalars().first()
            self.logger.info(f"New user ID: {new_user_id}")
            await self.set_user_base_role(session, new_user_id, chat_id)
            self.logger.info(f"base role was set for user: {new_user_id}")
            await session.commit()

        new_user = await self.get_user_by_id(new_user_id)
        self.logger.info(f"User created: {new_user}")
        return new_user


    async def get_users(self) -> list[User]:
        async with self.session_factory() as session:
            query_result = await session.execute(select(User))
            return query_result.scalars().all()


    async def get_user_by_id(self, user_id: int) -> User | None:
        query = select(User).where(User.id == user_id)
        async with self.session_factory() as session:
            query_result = await session.execute(query)
            user = query_result.scalars().first()
            return user

    async def get_user_by_username(self, username: str) -> User | None:
        async with self.session_factory() as session:
            # Сбрасываем кэш SQLAlchemy
            session.expire_all()
            user = await find_user_by_username(session, username)
            return user

    async def update_role_for_user(
            self,
            session: AsyncSession,
            user_id: int,
            new_role_name: str,
            chat_id: int
    ) -> None:
        self.logger.debug("Updating role for user: {user_id} in chat: {chat_id} to {new_role_name}")
        new_role_id:int = (
            await find_role_by_name(session,new_role_name)
        ).id
        self.logger.debug(f"New role ID: {new_role_id}")
        try:
            stmnt = (
                select(UserRoles)
                .where(
                    and_(
                            UserRoles.user_id == user_id,
                            UserRoles.chat_id == chat_id
                    )
                )
            )
            user_role: UserRoles | None = (
                await session.execute(stmnt)
            ).scalar_one_or_none()
            if user_role is None:
                 session.add(
                    UserRoles(
                        user_id=user_id,
                        chat_id=chat_id,
                        role_id=new_role_id
                    )
                )
            else:

                user_role.role_id = new_role_id

                await session.refresh(user_role)

        except IntegrityError:
            await session.rollback()
            raise UserRoleHasAlreadyBeenEstablishedException
        except Exception as e:
            self.logger.error(str(e))
        else:
            await session.commit()


    async def set_user_to_admin(self, session: AsyncSession, user_id: int, chat_id: int):
        await self.update_role_for_user(session, user_id, chat_id=chat_id, new_role_name="admin")

    async def set_user_base_role(self, session: AsyncSession, user_id: int, chat_id: int):
        await self.update_role_for_user(session, user_id, chat_id=chat_id, new_role_name="user")
