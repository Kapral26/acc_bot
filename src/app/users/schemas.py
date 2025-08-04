from pydantic import BaseModel

from src.app.users.chats.schemas import UserChatSchema


class UsersCreateSchema(BaseModel):
    id: int
    username: str
    first_name: str | None = None
    last_name: str | None = None
    chat: UserChatSchema | None = None

    class Config:
        from_attributes = True


class UserSchema(UsersCreateSchema):
    roles_id: int
    chats: list[UserChatSchema]


class UsersSchemaWithoutChat(BaseModel):
    id: int
    username: str
    first_name: str | None = None
    last_name: str | None = None
    roles_id: int

    class Config:
        from_attributes = True
