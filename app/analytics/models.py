from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.settings.database.database import Base


class Analytics(Base):
    __tablename__ = "analytics"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    who_send_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    bad_phrase_id: Mapped[int] = mapped_column(ForeignKey("bad_phrases.id"), nullable=False)
    users = relationship(
        "User", foreign_keys=[user_id], back_populates="analytics_as_user"
    )
    who_send = relationship(
        "User", foreign_keys=[who_send_id], back_populates="analytics_who_sent"
    )
