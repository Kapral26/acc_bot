from dataclasses import dataclass

from app.analytics.repository import AnalyticsRepository
from app.roles.schemas import RoleCRUD, RoleSchema
from app.users.schemas import UsersCreateSchema


@dataclass
class AnalyticsService:
    analytics_repository: AnalyticsRepository

    async def track_user_request(self, username: UsersCreateSchema, who_send: UsersCreateSchema) -> RoleSchema:
        new_role = await self.analytics_repository.track_user_request(who_send)
        return RoleSchema.model_validate(new_role)

