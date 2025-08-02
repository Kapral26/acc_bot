from asyncio import gather
from dataclasses import dataclass

from app.analytics.bad_phrase.schemas import BadPhraseCRUD
from app.analytics.bad_phrase.service import BadPhraseService
from app.analytics.repository import AnalyticsRepository
from app.users.schemas import UsersCreateSchema
from app.users.service import UserService


@dataclass
class AnalyticsService:
    analytics_repository: AnalyticsRepository
    user_service: UserService
    bad_phrase_service: BadPhraseService

    async def russian_roulette(self, who_send: UsersCreateSchema) -> BadPhraseCRUD:
        tasks = [
            self.user_service.get_random_user(who_send.chat.id),
            self.user_service.get_user_by_username(who_send.username),
            self.bad_phrase_service.get_random_bad_phrase(),
        ]

        user, who_send, random_bad_phrase_result = await gather(*tasks)
        await self.analytics_repository.track_user_request(
            user, who_send, random_bad_phrase_result
        )
        return BadPhraseCRUD(
            phrase=random_bad_phrase_result.phrase.replace("@", f"@{user.username}")
        )
