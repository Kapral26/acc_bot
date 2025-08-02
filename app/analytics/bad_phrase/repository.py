# repository.py — Репозиторий для работы с запрещёнными фразами (BadPhrase)

from collections.abc import Callable
from dataclasses import dataclass
from typing import TypeVar

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.analytics.bad_phrase.models import BadPhrase
from app.analytics.bad_phrase.schemas import BadPhraseCRUD
from app.exceptions import (
    RoleNotFoundException,  # Можно создать BadPhraseNotFoundException по аналогии
)

T = TypeVar("T")



@dataclass
class BadPhraseRepository:
    session_factory: Callable[[T], AsyncSession]

    async def get_random_bad_phrase(self) -> BadPhrase | None:
        async with self.session_factory() as session:
            stmt = select(BadPhrase).order_by(func.random()).limit(1)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def _get_bad_phrase_by_id(
        self, session: AsyncSession, bad_phrase_id: int
    ) -> BadPhrase | None:
        stmt = select(BadPhrase).where(BadPhrase.id == bad_phrase_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_bad_phrase(self, bad_phrase: BadPhraseCRUD):
        async with self.session_factory() as session:
            new_bad_phrase = BadPhrase(phrase=bad_phrase.phrase)
            session.add(new_bad_phrase)
            await session.commit()
            await session.refresh(new_bad_phrase)
            return new_bad_phrase

    async def get_bad_phrase_by_id(self, bad_phrase_id: int):
        async with self.session_factory() as session:
            bad_phrase = await self._get_bad_phrase_by_id(session, bad_phrase_id)
            if not bad_phrase:
                raise RoleNotFoundException  # Лучше создать BadPhraseNotFoundException
            return bad_phrase

    async def get_bad_phrase_by_phrase(self, phrase: str):
        async with self.session_factory() as session:
            stmt = select(BadPhrase).where(BadPhrase.phrase == phrase)
            result = await session.execute(stmt)
            bad_phrase = result.scalar_one_or_none()
            if not bad_phrase:
                raise RoleNotFoundException
            return bad_phrase

    async def get_bad_phrases(self):
        async with self.session_factory() as session:
            bad_phrases = await session.execute(select(BadPhrase))
            if not bad_phrases:
                raise RoleNotFoundException
            return bad_phrases.scalars().all()

    async def update_bad_phrase(self, bad_phrase_id: int, bad_phrase: BadPhraseCRUD):
        async with self.session_factory() as session:
            db_bad_phrase = await self._get_bad_phrase_by_id(session, bad_phrase_id)
            if not db_bad_phrase:
                raise RoleNotFoundException
            for key, value in bad_phrase.model_dump(exclude_unset=True).items():
                setattr(db_bad_phrase, key, value)
            await session.commit()
            await session.refresh(db_bad_phrase)
            return db_bad_phrase

    async def delete_bad_phrase(self, bad_phrase_id: int):
        async with self.session_factory() as session:
            db_bad_phrase = await self._get_bad_phrase_by_id(session, bad_phrase_id)
            if not db_bad_phrase:
                raise RoleNotFoundException
            await session.delete(db_bad_phrase)
            await session.commit()