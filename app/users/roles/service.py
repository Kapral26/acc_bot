from dataclasses import dataclass

from app.users.roles.repository import RolesRepository
from app.users.roles.schemas import RoleSchema


@dataclass
class RolesService:
    roles_repository: RolesRepository

    async def get_role_name_by_id(self, role_id: int) -> str:
        role_name = await self.roles_repository.get_role_name_by_id(role_id)
        return role_name

    async def get_role_id_by_name(self, role_name: str) -> int:
        role_id = await self.roles_repository.get_role_id_by_name(role_name)
        return role_id

    async def get_roles(self) -> list[RoleSchema]:
        roles = await self.roles_repository.get_roles()
        return roles
