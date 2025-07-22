from collections.abc import Callable
from dataclasses import dataclass
from typing import TypeVar

from sqlalchemy.ext.asyncio.session import AsyncSession

from app.exceptions import RoleNotFoundException
from app.roles.models import Role
from app.roles.schemas import RoleCreate, RoleSchema

T = TypeVar("T")

@dataclass
class RolesRepository:
    session_factory: Callable[[T], AsyncSession]

    async def create_role(self, role: RoleCreate):
        async with self.session_factory() as session:
            new_role = Role(name=role.name)
            session.add(new_role)
            await session.commit()
            await session.refresh(new_role)  # Для асинхронного SQLAlchemy
            return new_role

    async def get_roles_by_id(self, id: int):
        async with self.session_factory() as session:
            role = await session.get(Role.id == id)
            if not role:
                raise RoleNotFoundException
            return role

    async def get_roles_by_name(self, name: str):
        async with self.session_factory() as session:
            role = await session.get(Role.name == name)
            if not role:
                raise RoleNotFoundException
            return role

    async def get_roles(self):
        async with self.session_factory() as session:
            roles = await session.get(Role)
            if not roles:
                raise RoleNotFoundException
            return roles

    async def update_role(self, role: RoleSchema):
        async with self.session_factory() as session:
            db_role = await session.get(Role).filter(Role.id == role.id).first()
        if not db_role:
            raise RoleNotFoundException
        for key, value in role.model_dump().items():
            setattr(db_role, key, value)
        await session.commit()
        await session.refresh(db_role)
        return db_role


    async def delete_role(self, role_id: int):
        async with self.session_factory() as session:
            await session.delete(Role(id=role_id))
