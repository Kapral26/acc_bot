from pydantic import BaseModel


class UserChatCheckResponse(BaseModel):
    in_chat: bool
    detail: str | None = "Пользователь зарегистрирован в чате."
