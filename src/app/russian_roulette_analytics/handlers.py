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
    user_stats = await analytics_service.get_user_stats(user_id)
    return user_stats
