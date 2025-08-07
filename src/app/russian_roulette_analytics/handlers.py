from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from starlette import status

from src.app.russian_roulette_analytics.service import AnalyticsService
from src.app.users.schemas import UsersCreateSchema

router = APIRouter(prefix="/russian_roulette", tags=["Russian_Roulette"])


@router.post("/", status_code=status.HTTP_202_ACCEPTED)
@inject
async def russian_roulette(
    analytics_service: FromDishka[AnalyticsService],
    who_send: UsersCreateSchema,
):
    bad_phrase = await analytics_service.track_user_request(who_send)
    return bad_phrase


#
#
# @router.get("/analytics", status_code=status.HTTP_200_OK)
# @inject
# async def get_analytics(
#     analytics_service: FromDishka[AnalyticsService],
#     user_data: UsersCreateSchema,
# ):
#     bad_phrase = await analytics_service.get_analytics(user_data)
#     return bad_phrase


@router.get("/analytics/{user_id}", status_code=status.HTTP_200_OK)
@inject
async def get_count_user_send(
    analytics_service: FromDishka[AnalyticsService],
    user_id: int,
):
    aa = await analytics_service.get_user_stats(user_id)
    prime = {
        "activity": {"total_actions": 161, "total_received": 70, "total_sent": 91},
        "favorite_phrases": {
            "favorite_received": [(29, 5), (24, 4), (13, 4), (18, 4), (31, 4)],
            "favorite_sent": [(13, 6), (29, 6), (18, 5), (24, 5), (31, 5)],
        },
        "rank_in_chats": [(-1002655431803, 1), (471077141, 1)],
        "top_partners": {
            "received_from": [(471077141, 70)],
            "sent_to": [(471077141, 70), (1618384128, 21)],
        },
    }
    return aa
