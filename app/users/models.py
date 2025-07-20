from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.settings.database.database import Base, intpk, str_64


class User(Base):
    __tablename__ = 'users'

    id: Mapped[intpk]
    username: Mapped[str_64]
    first_name: Mapped[str_64]
    full_name: Mapped[str] = mapped_column(String(128), nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)
    role_rel = relationship('roles', back_populates='users')


class Role(Base):
    __tablename__ = 'roles'

    id: Mapped[intpk]
    role_name = Mapped[str_64]
    users = relationship('User', back_populates='role_rel')



