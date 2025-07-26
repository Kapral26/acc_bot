from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.dependencies import get_chats_service
from app.users.chats.schemas import UserChatSchema, UserChatSchemaCRUD
from app.users.chats.service import ChatsService

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