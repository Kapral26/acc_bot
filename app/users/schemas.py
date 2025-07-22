from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    username: str
    first_name: str | None = None
    full_name: str
    role_id: int

    class Config:
        from_attributes = True


class UsersCreateSchema(BaseModel):
    username: str
    first_name: str | None = None
    full_name: str
    role_id: int
