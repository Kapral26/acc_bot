from dataclasses import dataclass

from app.users.chats.repository import ChatsRepository
from app.users.chats.schemas import UserChatSchema


@dataclass
class ChatsService:
    chats_repository: ChatsRepository

    async def register_chat(self, chat: UserChatSchema):
        return await self.chats_repository.register_chat(chat)

    async def get_chat_by_id(self, chat_id: int):
        return await self.chats_repository.get_chat_by_id(chat_id)

    async def get_chat_by_title(self, title: str):
        return await self.chats_repository.get_chat_by_title(title)

    async def get_chats(self):
        return await self.chats_repository.get_chats()

    async def update_chat(self, chat_id: int, chat: UserChatSchema):
        return await self.chats_repository.update_chat(chat_id, chat)

    async def delete_chat(self, chat_id: int):
        await self.chats_repository.delete_chat(chat_id)
