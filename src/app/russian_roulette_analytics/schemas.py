from pydantic import BaseModel


class UserOverallStats(BaseModel):
    """
    Модель ответа с общей статистикой пользователя.

    Attributes:
        total_received: Общее количество полученных фраз.
        total_sent: Общее количество отправленных фраз.
        total_actions: Общее количество действий (получено + отправлено).

    """

    total_received: int
    total_sent: int
    total_actions: int


class ChatRank(BaseModel):
    """
    Модель для хранения информации о ранге пользователя в конкретном чате.

    Attributes:
        chat_id: Идентификатор чата.
        rank: Ранг пользователя в чате по количеству отправленных фраз.

    """

    chat_id: int
    title: str
    rank: int


class UserChatRanksResponse(BaseModel):
    """
    Модель ответа с рангами пользователя во всех чатах.

    Attributes:
        ranks: Список объектов с информацией о чате и ранге пользователя.

    """

    ranks: list[ChatRank]


class PhraseCount(BaseModel):
    phrase: str
    count: int


class FavoritePhrasesResponse(BaseModel):
    favorite_received: list[PhraseCount]
    favorite_sent: list[PhraseCount]


class UserCount(BaseModel):
    user: str
    count: int


class TopPartnersResponse(BaseModel):
    received_from: list[UserCount]
    sent_to: list[UserCount]


class UserStatisticRespone(BaseModel):
    activity: UserOverallStats
    rank_in_chats: UserChatRanksResponse
    favorite_phrases: FavoritePhrasesResponse
    top_partners: TopPartnersResponse
