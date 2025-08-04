from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from src.app.analytics.dependencies import get_analytics_service
from src.app.analytics.service import AnalyticsService
from src.app.settings.configs.settings import Settings
from src.app.users.schemas import UsersCreateSchema

router = APIRouter(prefix="/russian_roulette", tags=["Russian_Roulette"])
settings = Settings()


@router.post("/", status_code=status.HTTP_202_ACCEPTED)
async def russian_roulette(
    analytics_service: Annotated[AnalyticsService, Depends(get_analytics_service)],
    who_send: UsersCreateSchema,
):
    bad_phrase = await analytics_service.russian_roulette(who_send)
    return bad_phrase
