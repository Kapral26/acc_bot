from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.settings.database.database import Base


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    users = relationship("User", back_populates="role_rel")
