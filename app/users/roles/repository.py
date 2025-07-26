from collections.abc import Callable
from dataclasses import dataclass
from typing import TypeVar

from app.exceptions import RoleNotFoundException
from app.users.roles.models import Role
from app.users.roles.schemas import RoleCRUD
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

T = TypeVar("T")

async def find_role_by_name(session: AsyncSession, role_name: str) -> Role:
    stmt = select(Role).where(Role.name == role_name)
    result = await session.execute(stmt)
    role = result.scalar_one_or_none()
    if not role:
        raise RoleNotFoundException
    return role

@dataclass
class RolesRepository:
    session_factory: Callable[[T], AsyncSession]

    async def _get_role_by_id(
        self, session: AsyncSession, role_id: int
    ) -> Role | None:
        stmt = select(Role).where(Role.id == role_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_role(self, role: RoleCRUD):
        async with self.session_factory() as session:
            new_role = Role(name=role.name)
            session.add(new_role)
            await session.commit()
            await session.refresh(new_role)  # Для асинхронного SQLAlchemy
            return new_role

    async def get_roles_by_id(self, role_id: int):
        async with self.session_factory() as session:
            role = await self._get_role_by_id(session, role_id)
            if not role:
                raise RoleNotFoundException
            return role

    async def get_roles_by_name(self, role_name: str) -> Role:
        async with self.session_factory() as session:
            role = await find_role_by_name(session, role_name)
            return role

    async def get_roles(self):
        async with self.session_factory() as session:
            roles = await session.execute(select(Role))
            if not roles:
                raise RoleNotFoundException
            return roles.scalars().all()

    async def update_role(self, role_id:int, role: RoleCRUD):
        async with self.session_factory() as session:
            db_role = await self._get_role_by_id(session, role_id)
            if not db_role:
                raise RoleNotFoundException
            for key, value in role.model_dump(exclude_unset=True).items():
                setattr(db_role, key, value)
            await session.commit()
            await session.refresh(db_role)
            return db_role

    async def delete_role(self, role_id: int):
        async with self.session_factory() as session:
            db_role = await self._get_role_by_id(session, role_id)
            if not db_role:
                raise RoleNotFoundException
            await session.delete(db_role)
            await session.commit()
