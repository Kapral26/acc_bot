
from app.users.chats.enums import ChatTypeEnum
from pydantic import BaseModel


class UserChatSchema(BaseModel):
    id: int
    title: str | None
    type: ChatTypeEnum

    class Config:
        from_attributes = True

