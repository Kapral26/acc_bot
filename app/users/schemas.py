from pydantic import BaseModel


class UsersCreateSchema(BaseModel):
    username: str
    first_name: str | None = None
    last_name: str | None = None
    role_id: int = 3

    class Config:
        from_attributes = True


class UserSchema(UsersCreateSchema):
    id: int
