from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.settings.database.database import Base
from app.users.chats.enums import ChatTypeEnum


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(128), nullable=True)
    type: Mapped[ChatTypeEnum] = mapped_column(nullable=False)
    users = relationship(
        "User",
        secondary="user_chats",
        back_populates="chats"
    )
