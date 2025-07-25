from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.settings.database.database import Base
from app.users.enums import LocalUserChat


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(64), nullable=False)
    first_name: Mapped[str] = mapped_column(String(64))
    last_name: Mapped[str] = mapped_column(String(128), nullable=True)
    chat_id: Mapped[int] = mapped_column(Integer, default=LocalUserChat.id.value, nullable=True)
    roles = relationship(
        "Role",
        secondary="user_roles",
        back_populates="users",
    )
    analytics_as_user = relationship(
        "Analytics", foreign_keys="[Analytics.user_id]", back_populates="users"
    )
    analytics_who_sent = relationship(
        "Analytics", foreign_keys="[Analytics.who_send_id]", back_populates="who_send"
    )

    __table_args__ = (
        UniqueConstraint(
   "username",
            "chat_id",
            name="uq_username_chat_id"
        ),
    )


class UserRoles(Base):
    __tablename__ = "user_roles"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
