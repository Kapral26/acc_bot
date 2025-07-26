from dataclasses import dataclass

from app.analytics.bad_phrase.schemas import BadPhraseCRUD
from app.analytics.repository import AnalyticsRepository
from app.users.schemas import UsersCreateSchema


@dataclass
class AnalyticsService:
    analytics_repository: AnalyticsRepository

    async def track_user_request(self, who_send: UsersCreateSchema) -> BadPhraseCRUD:
        track_result = await self.analytics_repository.track_user_request(who_send)
        return BadPhraseCRUD.model_validate(track_result)

