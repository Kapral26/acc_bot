from dishka import Provider, Scope, provide

from src.app.users.roles.repository import RolesRepository
from src.app.users.roles.service import RolesService


class RolesProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_roles_repository(self) -> RolesRepository:
        return RolesRepository()

    @provide(scope=Scope.REQUEST)
    def get_roles_service(
        self,
        roles_repository: RolesRepository,
    ) -> RolesService:
        return RolesService(roles_repository=roles_repository)
