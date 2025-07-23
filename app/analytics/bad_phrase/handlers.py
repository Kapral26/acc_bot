# handlers.py — Обработчики (endpoints) для работы с запрещёнными фразами (bad_phrase)

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.analytics.bad_phrase.schemas import BadPhraseCRUD, BadPhraseSchema
from app.analytics.bad_phrase.service import BadPhraseService
from app.dependencies import get_bad_phrase_service

router = APIRouter(
    prefix="/bad-phrases",
    tags=["bad_phrase"],
)

# Получить все запрещённые фразы
@router.get("/", response_model=list[BadPhraseSchema])
async def get_bad_phrases(
    bad_phrase_service: Annotated[BadPhraseService, Depends(get_bad_phrase_service)],
):
    try:
        bad_phrases = await bad_phrase_service.get_bad_phrases()
    except Exception as error:
        raise HTTPException(status_code=422, detail=str(error))
    return bad_phrases

# Получить одну запрещённую фразу по id
@router.get("/by-id/{bad_phrase_id}", response_model=BadPhraseSchema)
async def get_bad_phrase_by_id(
    bad_phrase_id: int,
    bad_phrase_service: Annotated[BadPhraseService, Depends(get_bad_phrase_service)],
):
    try:
        bad_phrase = await bad_phrase_service.get_bad_phrase_by_id(bad_phrase_id)
    except Exception as error:
        raise HTTPException(status_code=422, detail=str(error))
    return bad_phrase

# Получить одну запрещённую фразу по тексту
@router.get("/by-phrase/{phrase}", response_model=BadPhraseSchema)
async def get_bad_phrase_by_phrase(
    phrase: str,
    bad_phrase_service: Annotated[BadPhraseService, Depends(get_bad_phrase_service)],
):
    try:
        bad_phrase = await bad_phrase_service.get_bad_phrase_by_phrase(phrase)
    except Exception as error:
        raise HTTPException(status_code=422, detail=str(error))
    return bad_phrase

# Создать новую запрещённую фразу
@router.post("/", response_model=BadPhraseSchema, status_code=status.HTTP_201_CREATED)
async def create_bad_phrase(
    bad_phrase: BadPhraseCRUD,
    bad_phrase_service: Annotated[BadPhraseService, Depends(get_bad_phrase_service)],
):
    try:
        new_bad_phrase = await bad_phrase_service.create_bad_phrase(bad_phrase)
    except Exception as error:
        raise HTTPException(status_code=422, detail=str(error))
    return new_bad_phrase

# Обновить запрещённую фразу
@router.put("/{bad_phrase_id}", response_model=BadPhraseSchema, status_code=status.HTTP_200_OK)
async def update_bad_phrase(
    bad_phrase_id: int,
    bad_phrase: BadPhraseCRUD,
    bad_phrase_service: Annotated[BadPhraseService, Depends(get_bad_phrase_service)],
):
    try:
        updated_bad_phrase = await bad_phrase_service.update_bad_phrase(bad_phrase_id, bad_phrase)
    except Exception as error:
        raise HTTPException(status_code=404, detail=str(error))
    return updated_bad_phrase

# Удалить запрещённую фразу
@router.delete("/{bad_phrase_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bad_phrase(
    bad_phrase_id: int,
    bad_phrase_service: Annotated[BadPhraseService, Depends(get_bad_phrase_service)],
):
    try:
        await bad_phrase_service.delete_bad_phrase(bad_phrase_id)
    except Exception as error:
        raise HTTPException(status_code=404, detail=str(error))