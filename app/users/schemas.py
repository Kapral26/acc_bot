from pydantic import BaseModel

from app.users.chats.schemas import UserChatSchema


class UsersCreateSchema(BaseModel):
    username: str
    first_name: str | None = None
    last_name: str | None = None
    role_id: int = 3
    chat: UserChatSchema

    class Config:
        from_attributes = True


class UserSchema(UsersCreateSchema):
    id: int
