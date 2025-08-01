
from enum import Enum

from pydantic import BaseModel


class RoleKey(int, Enum):
    user = 1
    admin = 2

class RoleValue(str, Enum):
    user = "user"
    admin="admin"


class RoleSchema(BaseModel):
    id: RoleKey
    name: RoleValue

    @classmethod
    def get_description(cls):
        info = "Можно использовать только значения:\n"
        return info + "\n".join([f"{x.value}: {x.name}" for x in RoleKey])
