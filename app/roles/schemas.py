
from pydantic import BaseModel


class RoleSchema(BaseModel):
    id: int
    role_name: str

    class Config:
        from_attributes = True
class RoleCreate(BaseModel):
    role_name: str

    class Config:
        from_attributes = True
