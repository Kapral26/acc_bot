from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any

from sqlalchemy import Row, func, select
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute, aliased

from src.app.russian_roulette_analytics.bad_phrase.models import BadPhrase
from src.app.russian_roulette_analytics.models import Analytics
from src.app.users.chats.models import Chat
from src.app.users.models import User
from src.app.users.schemas import UserSchema, UsersCreateSchema


@dataclass
class AnalyticsRepository:
    """
    Репозиторий для работы с аналитикой.

    Attributes:
        session_factory: Фабрика асинхронных сессий SQLAlchemy.

    """

    session_factory: Callable[[], AsyncSession]

    async def track_user_request(
        self,
        user: UserSchema,
        who_send: UsersCreateSchema,
        random_bad_phrase_result: BadPhrase,
    ) -> None:
        """
        Записывает информацию о пользовательском запросе в базу данных.

        Args:
            user: Схема пользователя, которому был отправлен запрос.
            who_send: Схема пользователя, который отправил запрос.
            random_bad_phrase_result: Объект плохой фразы, которая была использована.

        """
        async with self.session_factory() as session:
            analytic_item = Analytics(
                user_id=user.id,
                bad_phrase_id=random_bad_phrase_result.id,
                who_send_id=who_send.id,
                chat_id=who_send.chat.id,
            )
            session.add(analytic_item)
            await session.commit()

    async def get_total_sent(self, user_id: int) -> int:
        """
        Возвращает количество раз, когда пользователь отправлял фразы другим пользователям.

        Args:
            user_id: Идентификатор пользователя.

        Returns:
            Количество отправок.

        """
        count_user_send = await self._get_count_user_statistic(
            user_id, field=Analytics.who_send_id
        )
        return count_user_send

    async def get_total_received(self, user_id: int) -> int:
        """
        Возвращает количество раз, когда пользователь получал фразы от других.

        Args:
            user_id: Идентификатор пользователя.

        Returns:
            Количество полученных фраз.

        """
        count_user_was_tracked = await self._get_count_user_statistic(
            user_id, field=Analytics.user_id
        )
        return count_user_was_tracked

    async def _get_count_user_statistic(
        self, user_id: int, field: InstrumentedAttribute
    ) -> int:
        """
        Вспомогательный метод для получения статистики пользователя по указанному полю.

        Args:
            user_id: Идентификатор пользователя.
            field: Поле модели Analytics для фильтрации.

        Returns:
            Количество записей, соответствующих критерию.

        """
        async with self.session_factory() as session:
            stmnt = select(func.count(Analytics.id)).where(field == user_id)
            result = await session.execute(stmnt)
            return result.scalar()

    async def get_user_rank_in_chats(self, user_id: int) -> list[tuple[int, int]]:
        """
        Возвращает ранг пользователя в чатах по количеству отправленных фраз.

        Args:
            user_id: Идентификатор пользователя.

        Returns:
            Список кортежей (ID чата, ранг пользователя в чате).

        """
        async with self.session_factory() as session:
            analytics_alias = aliased(Analytics)
            subq = (
                select(
                    analytics_alias.chat_id,
                    Chat.title,
                    analytics_alias.who_send_id,
                    func.count(analytics_alias.id).label("send_count"),
                    func.rank()
                    .over(
                        partition_by=analytics_alias.chat_id,
                        order_by=func.count(analytics_alias.id).desc(),
                    )
                    .label("rank"),
                )
                .where(analytics_alias.who_send_id == user_id)
                .join(Chat, analytics_alias.chat_id == Chat.id)
                .group_by(
                    analytics_alias.chat_id, Chat.title, analytics_alias.who_send_id
                )
                .subquery()
            )
            final_query = select(subq.c.chat_id, subq.c.title, subq.c.rank)
            result = await session.execute(final_query)
            return result.all()

    async def get_user_favorite_phrases(
        self, user_id: int
    ) -> dict[str, Sequence[Row[tuple[int, Any]]]]:
        """
        Возвращает топ-5 любимых фраз пользователя, как полученных, так и отправленных.

        Args:
            user_id: Идентификатор пользователя.

        Returns:
            Словарь с ключами "favorite_received" и "favorite_sent", содержащий списки кортежей (ID фразы, количество).

        """
        async with self.session_factory() as session:
            received_phrases = (
                select(BadPhrase.phrase, func.count(Analytics.id))
                .where(Analytics.user_id == user_id)
                .join(BadPhrase, BadPhrase.id == Analytics.bad_phrase_id)
                .group_by(BadPhrase.phrase)
                .order_by(func.count(Analytics.id).desc())
                .limit(5)
            )

            sent_phrases = (
                select(BadPhrase.phrase, func.count(Analytics.id))
                .where(Analytics.who_send_id == user_id)
                .join(BadPhrase, BadPhrase.id == Analytics.bad_phrase_id)
                .group_by(BadPhrase.phrase)
                .order_by(func.count(Analytics.id).desc())
                .limit(5)
            )

            received_result = await session.execute(received_phrases)
            sent_result = await session.execute(sent_phrases)

            return {
                "favorite_received": received_result.all(),
                "favorite_sent": sent_result.all(),
            }

    async def get_user_top_partners(
        self, user_id: int
    ) -> dict[str, Sequence[Row[tuple[int, Any]]]]:
        """
        Возвращает топ-5 пользователей, чаще всего взаимодействовавших с данным пользователем.

        Args:
            user_id: Идентификатор пользователя.

        Returns:
            Словарь с ключами "sent_to" и "received_from", где содержится список пар (ID пользователя, количество взаимодействий).

        """
        async with self.session_factory() as session:
            # Кто чаще получал от него
            who_received_from_user = (
                select(User.username, func.count(Analytics.id))
                .where(Analytics.who_send_id == user_id)
                .join(User, User.id == Analytics.user_id)
                .group_by(User.username)
                .order_by(func.count(Analytics.id).desc())
                .limit(5)
            )

            # Кто чаще присылал ему
            who_sent_to_user = (
                select(User.username, func.count(Analytics.id))
                .where(Analytics.user_id == user_id)
                .join(User, User.id == Analytics.who_send_id)
                .group_by(User.username)
                .order_by(func.count(Analytics.id).desc())
                .limit(5)
            )

            result1 = await session.execute(who_received_from_user)
            result2 = await session.execute(who_sent_to_user)

            return {"sent_to": result1.all(), "received_from": result2.all()}

    async def get_top_users(self) -> list[tuple[int, int]]:
        """
        Возвращает топ-5 пользователей по общему количеству взаимодействий.

        Returns:
            Список кортежей (ID пользователя, количество взаимодействий).

        """
        async with self.session_factory() as session:
            top_users = (
                select(Analytics.user_id, func.count(Analytics.id))
                .group_by(Analytics.user_id)
                .order_by(func.count(Analytics.id).desc())
                .limit(5)
            )
            result = await session.execute(top_users)
            return result.all()
