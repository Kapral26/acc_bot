from pydantic import BaseModel

from app.users.chats.schemas import UserChatSchema


class UsersCreateSchema(BaseModel):
    id: int
    username: str
    first_name: str | None = None
    last_name: str | None = None
    chat: UserChatSchema

    class Config:
        from_attributes = True


class UserSchema(UsersCreateSchema):
    role_id: int

class UserWasCreated(BaseModel):
    text: str = "Пользователь был создан"
