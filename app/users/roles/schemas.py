
from pydantic import BaseModel


class RoleSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
class RoleCRUD(BaseModel):
    name: str

    class Config:
        from_attributes = True
