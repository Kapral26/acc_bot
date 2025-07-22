from dataclasses import dataclass

from app.roles.repository import RolesRepository
from app.roles.schemas import RoleSchema, RoleCreate


@dataclass
class RolesService:
    roles_repository: RolesRepository

    async def create_role(self, role: RoleCreate):
        new_role = await self.roles_repository.create_role(role)
        return new_role

    async def get_role_by_name(self, name: str):
        role = await self.roles_repository.get_roles_by_name(name)
        return role

    async def get_role_by_id(self, role_id: int):
        role = await self.roles_repository.get_roles_by_id(role_id)
        return role

    async def get_roles(self) -> list[RoleSchema]:
        roles = await self.roles_repository.get_roles()
        return [RoleSchema.model_validate(x) for x in roles]

    async def delete_role(self, role_id: int):
        await self.roles_repository.delete_role(role_id)
