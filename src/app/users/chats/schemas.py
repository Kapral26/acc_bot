from pydantic import BaseModel

from src.app.users.chats.enums import ChatTypeEnum


class UserChatSchemaCRUD(BaseModel):
    title: str | None
    type: ChatTypeEnum

    class Config:
        from_attributes = True


class UserChatSchema(UserChatSchemaCRUD):
    id: int
