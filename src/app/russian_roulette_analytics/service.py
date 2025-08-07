import asyncio
from asyncio import gather
from dataclasses import dataclass

from src.app.russian_roulette_analytics.bad_phrase.schemas import BadPhraseCRUD
from src.app.russian_roulette_analytics.bad_phrase.service import BadPhraseService
from src.app.russian_roulette_analytics.repository import AnalyticsRepository
from src.app.russian_roulette_analytics.schemas import (
    ChatRank,
    FavoritePhrasesResponse,
    TopPartnersResponse,
    UserChatRanksResponse,
    UserOverallStats,
    UserStatisticRespone,
)
from src.app.users.schemas import UsersCreateSchema
from src.app.users.service import UserService


@dataclass
class AnalyticsService:
    analytics_repository: AnalyticsRepository
    user_service: UserService
    bad_phrase_service: BadPhraseService

    async def track_user_request(self, who_send: UsersCreateSchema) -> BadPhraseCRUD:
        tasks = [
            self.user_service.get_random_user(who_send.chat.id),
            self.bad_phrase_service.get_random_bad_phrase(),
        ]

        user, random_bad_phrase_result = await gather(*tasks)
        await self.analytics_repository.track_user_request(
            user, who_send, random_bad_phrase_result
        )
        return BadPhraseCRUD(
            phrase=random_bad_phrase_result.phrase.replace("@", f"@{user.username}")
        )

    async def get_user_total_activity(self, user_id: int) -> UserOverallStats:
        total_received = await self.analytics_repository.get_total_received(user_id)
        total_sent = await self.analytics_repository.get_total_sent(user_id)

        return UserOverallStats(
            total_received=total_received,
            total_sent=total_sent,
            total_actions=total_received + total_sent,
        )

    async def get_analytics(self, user_data: UsersCreateSchema):
        user = self.user_service.get_user_by_id(user_data.id)

    async def get_user_stats(self, user_id: int) -> UserStatisticRespone:
        results = await asyncio.gather(
            self.get_user_total_activity(user_id),
            self.get_user_rank_in_chats(user_id),
            self.get_user_favorite_phrases(user_id),
            self.get_user_top_partners(user_id),
        )

        activity, rank_in_chats, favorite_phrases, top_partners = results

        return UserStatisticRespone(
            activity=activity,
            rank_in_chats=rank_in_chats,
            favorite_phrases=favorite_phrases,
            top_partners=top_partners,
        )

    async def get_user_top_partners(self, user_id: int) -> TopPartnersResponse:
        data = await self.analytics_repository.get_user_top_partners(user_id)
        converted_data = {
            "received_from": [
                {"user": u, "count": c} for u, c in data["received_from"]
            ],
            "sent_to": [{"user": u, "count": c} for u, c in data["sent_to"]],
        }
        top_partners = TopPartnersResponse(**converted_data)
        return top_partners

    async def get_user_favorite_phrases(self, user_id: int) -> FavoritePhrasesResponse:
        data = await self.analytics_repository.get_user_favorite_phrases(user_id)
        converted_data = {
            "favorite_received": [
                {"phrase": p, "count": c} for p, c in data["favorite_received"]
            ],
            "favorite_sent": [
                {"phrase": p, "count": c} for p, c in data["favorite_sent"]
            ],
        }
        favorite_phrases = FavoritePhrasesResponse(**converted_data)
        return favorite_phrases

    async def get_user_rank_in_chats(self, user_id: int) -> UserChatRanksResponse:
        rank_raws = await self.analytics_repository.get_user_rank_in_chats(user_id)
        chat_ranks = [
            ChatRank(chat_id=chat_id, title=title, rank=rank)
            for chat_id, title, rank in rank_raws
        ]
        rank_in_chats = UserChatRanksResponse(ranks=chat_ranks)
        return rank_in_chats
