from asyncio import gather
from collections.abc import Callable
from dataclasses import dataclass
from typing import TypeVar

from sqlalchemy.ext.asyncio.session import AsyncSession

from app.analytics.bad_phrase.repository import get_random_bad_phrase
from app.analytics.bad_phrase.schemas import BadPhraseCRUD
from app.analytics.models import Analytics
from app.exceptions import BadPhraseNotFoundError
from app.users.exceptions import UserNotFoundError
from app.users.schemas import UsersCreateSchema

T = TypeVar("T")

@dataclass
class AnalyticsRepository:
    session_factory: Callable[[T], AsyncSession]

    async def track_user_request(self, who_send: UsersCreateSchema) -> BadPhraseCRUD:
        async with self.session_factory() as session:
            tasks = [
                get_random_user(session),
                find_user_by_username(session, who_send.username),
                get_random_bad_phrase(session),
            ]

            user, who_send, random_bad_phrase_result = gather(*tasks)
            if not user:
                raise UserNotFoundError
            if not random_bad_phrase_result:
                raise BadPhraseNotFoundError
            req_result = BadPhraseCRUD(phrase = random_bad_phrase_result.phrase.replace("@", f"@{user.username}"))
            analytic_item = Analytics(
                user_id=user.id,
                bad_phrase_id=random_bad_phrase_result.id,
                who_send_id=who_send.id,
            )
            session.add(analytic_item)
            await session.commit()
            return req_result
