from pydantic import BaseModel
from typing import Optional

class UserData(BaseModel):
    user_id: int
    username: str | None
    first_name: str | None
    last_name: str | None
    chat_id: int