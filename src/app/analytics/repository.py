from collections.abc import Callable
from dataclasses import dataclass
from typing import TypeVar

from sqlalchemy.ext.asyncio.session import AsyncSession

from src.app.analytics.bad_phrase.models import BadPhrase
from src.app.analytics.models import Analytics
from src.app.users.schemas import UserSchema, UsersCreateSchema

T = TypeVar("T")


@dataclass
class AnalyticsRepository:
    session_factory: Callable[[T], AsyncSession]

    async def track_user_request(
        self,
        user: UserSchema,
        who_send: UsersCreateSchema,
        random_bad_phrase_result: BadPhrase,
    ) -> None:
        async with self.session_factory() as session:
            analytic_item = Analytics(
                user_id=user.id,
                bad_phrase_id=random_bad_phrase_result.id,
                who_send_id=who_send.id,
                chat_id=who_send.chat.id,
            )
            session.add(analytic_item)
            await session.commit()
