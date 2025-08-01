from sqlalchemy import ForeignKey, String, \
    UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.settings.database.database import Base
from app.users.roles.schemas import RoleSchema


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(64), nullable=False)
    first_name: Mapped[str] = mapped_column(String(64))
    last_name: Mapped[str] = mapped_column(String(128), nullable=True)
    roles_id: Mapped[int] = mapped_column(
        comment=RoleSchema.get_description(), nullable=False, default=1
    )
    chats = relationship(
        "Chat",
        secondary="user_chats",
        back_populates="users",
    )
    analytics_as_user = relationship(
        "Analytics", foreign_keys="[Analytics.user_id]", back_populates="users"
    )
    analytics_who_sent = relationship(
        "Analytics", foreign_keys="[Analytics.who_send_id]", back_populates="who_send"
    )


class UserChats(Base):
    __tablename__ = "user_chats"
    __table_args__ = (UniqueConstraint("user_id", "chat_id", name="uq_user_chat"),)
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"))


