from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.settings.database.database import Base


class BadPhrase(Base):
    __tablename__ = "bad_phrases"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    phrase: Mapped[str] = mapped_column(String(1024), nullable=False)

