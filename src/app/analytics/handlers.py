from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from starlette import status

from src.app.analytics.service import AnalyticsService
from src.app.settings.configs.settings import Settings
from src.app.users.schemas import UsersCreateSchema

router = APIRouter(prefix="/russian_roulette", tags=["Russian_Roulette"])
settings = Settings()


@router.post("/", status_code=status.HTTP_202_ACCEPTED)
@inject
async def russian_roulette(
    analytics_service: FromDishka[AnalyticsService],
    who_send: UsersCreateSchema,
):
    bad_phrase = await analytics_service.russian_roulette(who_send)
    return bad_phrase
