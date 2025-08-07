from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, HTTPException
from starlette import status

from src.app.analytics.bad_phrase.schemas import BadPhraseCRUD, BadPhraseSchema
from src.app.analytics.bad_phrase.service import BadPhraseService

router = APIRouter(
    prefix="/bad-phrases",
    tags=["bad_phrase"],
)


# Получить все запрещённые фразы
@router.get("/", response_model=list[BadPhraseSchema])
@inject
async def get_bad_phrases(
    bad_phrase_service: FromDishka[BadPhraseService],
):
    try:
        bad_phrases = await bad_phrase_service.get_bad_phrases()
    except Exception as error:
        raise HTTPException(status_code=422, detail=str(error))
    return bad_phrases


# Получить одну запрещённую фразу по id
@router.get("/by-id/{bad_phrase_id}", response_model=BadPhraseSchema)
@inject
async def get_bad_phrase_by_id(
    bad_phrase_id: int,
    bad_phrase_service: FromDishka[BadPhraseService],
):
    try:
        bad_phrase = await bad_phrase_service.get_bad_phrase_by_id(bad_phrase_id)
    except Exception as error:
        raise HTTPException(status_code=422, detail=str(error))
    return bad_phrase


# Получить одну запрещённую фразу по тексту
@router.get("/by-phrase/{phrase}", response_model=BadPhraseSchema)
@inject
async def get_bad_phrase_by_phrase(
    phrase: str,
    bad_phrase_service: FromDishka[BadPhraseService],
):
    try:
        bad_phrase = await bad_phrase_service.get_bad_phrase_by_phrase(phrase)
    except Exception as error:
        raise HTTPException(status_code=422, detail=str(error))
    return bad_phrase


# Создать новую запрещённую фразу
@router.post("/", status_code=status.HTTP_201_CREATED)
@inject
async def create_bad_phrase(
    bad_phrase: BadPhraseCRUD,
    bad_phrase_service: FromDishka[BadPhraseService],
):
    await bad_phrase_service.create_bad_phrase(bad_phrase)


# Обновить запрещённую фразу
@router.put(
    "/{bad_phrase_id}", response_model=BadPhraseSchema, status_code=status.HTTP_200_OK
)
@inject
async def update_bad_phrase(
    bad_phrase_id: int,
    bad_phrase: BadPhraseCRUD,
    bad_phrase_service: FromDishka[BadPhraseService],
):
    try:
        updated_bad_phrase = await bad_phrase_service.update_bad_phrase(
            bad_phrase_id, bad_phrase
        )
    except Exception as error:
        raise HTTPException(status_code=404, detail=str(error))
    return updated_bad_phrase


# Удалить запрещённую фразу
@router.delete("/{bad_phrase_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_bad_phrase(
    bad_phrase_id: int,
    bad_phrase_service: FromDishka[BadPhraseService],
):
    try:
        await bad_phrase_service.delete_bad_phrase(bad_phrase_id)
    except Exception as error:
        raise HTTPException(status_code=404, detail=str(error))
