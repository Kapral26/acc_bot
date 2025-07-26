
from pydantic import BaseModel

from app.users.chats.enums import ChatTypeEnum


class UserChatSchema(BaseModel):
    id: int
    title: str | None
    type: ChatTypeEnum

    class Config:
        from_attributes = True

