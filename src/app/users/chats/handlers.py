from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from src.app.users.chats.dependencies import get_chats_service
from src.app.users.chats.schemas import UserChatSchema, UserChatSchemaCRUD
from src.app.users.chats.service import ChatsService
from src.app.users.exceptions import UserIsNotRegisteredIntoThisChat

router = APIRouter(
    prefix="/chats",
    tags=["chats"],
)


@router.get("/", response_model=list[UserChatSchema])
async def get_chats(
    chats_service: Annotated[ChatsService, Depends(get_chats_service)],
):
    try:
        chats = await chats_service.get_chats()
    except Exception as error:
        raise HTTPException(status_code=422, detail=str(error))
    return chats


@router.get("/{chat_id}", response_model=UserChatSchema)
async def get_chat_by_id(
    chat_id: int,
    chats_service: Annotated[ChatsService, Depends(get_chats_service)],
):
    try:
        chat = await chats_service.get_chat_by_id(chat_id)
    except Exception as error:
        raise HTTPException(status_code=404, detail=str(error))
    return chat


@router.get("/by-title/{title}", response_model=UserChatSchema)
async def get_chat_by_title(
    title: str,
    chats_service: Annotated[ChatsService, Depends(get_chats_service)],
):
    try:
        chat = await chats_service.get_chat_by_title(title)
    except Exception as error:
        raise HTTPException(status_code=404, detail=str(error))
    return chat


@router.post("/", response_model=UserChatSchema, status_code=status.HTTP_201_CREATED)
async def register_chat(
    chat: UserChatSchemaCRUD,
    chats_service: Annotated[ChatsService, Depends(get_chats_service)],
):
    try:
        new_chat = await chats_service.register_chat(chat)
    except Exception as error:
        raise HTTPException(status_code=422, detail=str(error))
    return new_chat


@router.put("/{chat_id}", response_model=UserChatSchema, status_code=status.HTTP_200_OK)
async def update_chat(
    chat_id: int,
    chat: UserChatSchemaCRUD,
    chats_service: Annotated[ChatsService, Depends(get_chats_service)],
):
    try:
        updated_chat = await chats_service.update_chat(chat_id, chat)
    except Exception as error:
        raise HTTPException(status_code=404, detail=str(error))
    return updated_chat


@router.delete("/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat(
    chat_id: int,
    chats_service: Annotated[ChatsService, Depends(get_chats_service)],
):
    try:
        await chats_service.delete_chat(chat_id)
    except Exception as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.get(
    "/{chat_id}/users/{user_id}",
    status_code=status.HTTP_200_OK,
)
async def is_user_in_chat(
    chat_id: int,
    user_id: int,
    chat_service: Annotated[ChatsService, Depends(get_chats_service)],
):
    user_exist_into_chat = await chat_service.is_user_in_chat(user_id, chat_id)
    if not user_exist_into_chat:
        raise UserIsNotRegisteredIntoThisChat

    return {"in_chat": True}
