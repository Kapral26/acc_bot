import logging
from collections.abc import Callable
from dataclasses import dataclass
from typing import TypeVar

from app.exceptions import RoleNotFoundException
from app.settings.configs.logger import log_function
from app.users.chats.models import Chat
from app.users.chats.schemas import UserChatSchema
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")

async def find_chat_by_id(
        session: AsyncSession, chat_id: int
    ) -> Chat | None:
        stmt = select(Chat.id).where(Chat.id == chat_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

async def create_new_chat(session: AsyncSession, chat: UserChatSchema) -> Chat:
    new_chat = Chat(**chat.model_dump(mode="json"))
    session.add(new_chat)
    await session.commit()
    await session.refresh(new_chat)
    return new_chat

async def get_chat_id(session: AsyncSession, chat: UserChatSchema) -> int:
    chat_id = await find_chat_by_id(session, chat.id)
    if not chat_id:
        create_result = await create_new_chat(session, chat)
        chat_id = create_result.id

    return chat_id

@dataclass
class ChatsRepository:
    session_factory: Callable[[T], AsyncSession]

    async def register_chat(self, chat: UserChatSchema):
        async with self.session_factory() as session:
            new_chat = await create_new_chat(session, chat)
            return new_chat

    async def get_chat_by_id(self, chat_id: int):
        async with self.session_factory() as session:
            chat = await find_chat_by_id(session, chat_id)
            if not chat:
                raise RoleNotFoundException  # Лучше создать ChatNotFoundException
            return chat

    async def get_chat_by_title(self, title: str):
        async with self.session_factory() as session:
            stmt = select(Chat).where(Chat.title == title)
            result = await session.execute(stmt)
            chat = result.scalar_one_or_none()
            if not chat:
                raise RoleNotFoundException
            return chat

    async def get_chats(self):
        async with self.session_factory() as session:
            chats = await session.execute(select(Chat))
            return chats.scalars().all()

    async def update_chat(self, chat_id: int, chat: UserChatSchema):
        async with self.session_factory() as session:
            db_chat = await find_chat_by_id(session, chat_id)
            if not db_chat:
                raise RoleNotFoundException
            for key, value in chat.model_dump(exclude_unset=True).items():
                if hasattr(db_chat, key):
                    setattr(db_chat, key, value)
            await session.commit()
            await session.refresh(db_chat)
            return db_chat

    async def delete_chat(self, chat_id: int):
        async with self.session_factory() as session:
            db_chat = await find_chat_by_id(session, chat_id)
            if not db_chat:
                raise RoleNotFoundException
            await session.delete(db_chat)
            await session.commit()
