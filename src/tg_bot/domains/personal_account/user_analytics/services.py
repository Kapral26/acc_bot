from dataclasses import dataclass

from aiogram import types

from src.app.russian_roulette_analytics.schemas import UserStatisticRespone
from src.app.users.schemas import UsersCreateSchema
from src.tg_bot.domains.personal_account.user_analytics.repository import (
    UserAnalyticsRepository,
)
from src.tg_bot.domains.user_management.services import extract_user_data


@dataclass
class UserAnalyticsService:
    user_analytics_repository: UserAnalyticsRepository

    @extract_user_data
    async def get_user_statistic_message(
        self,
        event: types.TelegramObject,
        user_data: UsersCreateSchema,
    ) -> str:
        user_statistic = await self.user_analytics_repository.get_user_statistic(
            user_data.id
        )
        model_user_stat = UserStatisticRespone.model_validate(user_statistic)

        return await self.build_user_stats_message(model_user_stat)

    async def build_user_stats_message(self, user_stat: UserStatisticRespone) -> str:
        message = "**📊 Статистика пользователя**:\n\n"

        # Активность
        activity = user_stat.activity
        message += f"▫️ Получено: {activity.total_received}\n"
        message += f"▫️ Отправлено: {activity.total_sent}\n"
        message += f"▫️ Всего действий: {activity.total_actions}\n\n"

        # Ранги в чатах
        message += "🏆 Ранги в чатах:\n"
        for rank in user_stat.rank_in_chats.ranks:
            message += f"- *{rank.title}*: #{rank.rank}\n"

        message += "\n💬 Топ фраз:\n"

        # Топ полученных фраз
        message += "📥 Получено:\n"
        for phrase in user_stat.favorite_phrases.favorite_received[:5]:
            message += f'- "{phrase.phrase}" ({phrase.count} раз)\n'

        # Топ отправленных фраз
        message += "\n📤 Отправлено:\n"
        for phrase in user_stat.favorite_phrases.favorite_sent[:5]:
            message += f'- "{phrase.phrase}" ({phrase.count} раз)\n'

        message += "\n🤝 Топ собеседники:\n"

        # Кто чаще всего отправлял пользователю
        message += "📩 Получено от:\n"
        for partner in user_stat.top_partners.received_from:
            message += f"- {partner.user}: {partner.count} раз\n"

        # К кому пользователь чаще всего отправлял
        message += "\n✉️ Отправлено кому:\n"
        for partner in user_stat.top_partners.sent_to:
            message += f"- {partner.user}: {partner.count} раз\n"

        return message
