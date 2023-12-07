from fastapi import APIRouter, status, Depends, status, Request

from src.application.chat_room.service import ChatRoomService
from src.dependencies.chat_room_dependencies import get_chat_room_service
from src.dependencies.auth_dependencies import get_current_user_id
from src.presentation.chat_room.dtos import (
    CreateRoomRequest,
    CreateRoomResponse,
    RoomNameRequest,
    ChangeRoomSetting,
    LeaveRoomRequest,
    SaveMessageRequest
)


router = APIRouter(
    prefix="/chat_room",
    tags=["chat_room"]  
)

########################################################################################## post ##########################################################################################

@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=CreateRoomResponse)
async def create_chat_room(
    request: CreateRoomRequest,
    chat_room_service: ChatRoomService = Depends(get_chat_room_service),
    current_user_id: str = Depends(get_current_user_id)
    ) -> CreateRoomResponse:
    new_chat_room_entity = chat_room_service.create_chat_room(
        room_name=request.room_name,
        tag=request.tag,
        maximum_people=request.maximum_people,
        user_id=current_user_id
        )
    
    return CreateRoomResponse(
        room_name=new_chat_room_entity.room_name,
        maximum_people=new_chat_room_entity.maximum_people,
        tag=new_chat_room_entity.tag
        )


@router.post('/save_message', status_code=status.HTTP_200_OK)
async def save_message(
    request: SaveMessageRequest,
    chat_room_service: ChatRoomService = Depends(get_chat_room_service),
    current_user_id: str = Depends(get_current_user_id)
    ) -> None:
    chat_room_service.save_message(
        room_name=request.room_name,
        user_name=request.user_name,
        content=request.content
        )


@router.post('/join_room', status_code=status.HTTP_200_OK)
async def join_room(
    request: RoomNameRequest,
    chat_room_service: ChatRoomService = Depends(get_chat_room_service),
    current_user_id: str = Depends(get_current_user_id)
    ) -> None:
    chat_room_service.join_room(
        room_name=request.room_name,
        user_id=current_user_id
        )

########################################################################################## delete ##########################################################################################

@router.delete('/delete', status_code=status.HTTP_200_OK)
async def delete_room(
    request: RoomNameRequest,    
    chat_room_service: ChatRoomService = Depends(get_chat_room_service),
    current_user_id: str = Depends(get_current_user_id)
    ) -> None:
    chat_room_service.delete_room(
        room_name=request.room_name,
        user_id=current_user_id
        )


@router.delete('/leave_room', status_code=status.HTTP_200_OK)
async def leave_room(
    request: LeaveRoomRequest,
    chat_room_service: ChatRoomService = Depends(get_chat_room_service),
    current_user_id: str = Depends(get_current_user_id)
    ) -> None:
    chat_room_service.leave_room(
        room_name=request.room_name,
        user_name=request.user_name,
        user_id=current_user_id
        )

########################################################################################## get ##########################################################################################

@router.get('/all_rooms_list', status_code=status.HTTP_200_OK)
async def get_all_rooms_list(
    chat_room_service: ChatRoomService = Depends(get_chat_room_service),
    current_user_id: str = Depends(get_current_user_id)
    ):
    
    room_list = chat_room_service.get_all_rooms_list()
    
    return room_list


@router.get('/rooms_list/{search_word}', status_code=status.HTTP_200_OK)
async def get_rooms_list(
    search_word: str,
    chat_room_service: ChatRoomService = Depends(get_chat_room_service),
    current_user_id: str = Depends(get_current_user_id)
    ):
    room_list = chat_room_service.get_rooms_list(search_word=search_word)
    
    return room_list


@router.get('/joined_rooms_list/{user_id}', status_code=status.HTTP_200_OK)
async def get_joined_rooms_list(
    chat_room_service: ChatRoomService = Depends(get_chat_room_service),
    current_user_id: str = Depends(get_current_user_id)
    ):
    
    user_in_room_list = chat_room_service.get_joined_rooms_list(user_id=current_user_id)

    return user_in_room_list


@router.get('/current_room_member_list/{room_name}', status_code=status.HTTP_200_OK)
async def get_current_room_member_list(
    room_name: str,
    chat_room_service: ChatRoomService = Depends(get_chat_room_service),
    current_user_id: str = Depends(get_current_user_id),
    ):
    room_members_list = chat_room_service.get_current_room_member_list(room_name=room_name)
    return room_members_list


@router.get('/message_history/{room_name}', status_code=status.HTTP_200_OK)
async def get_message_history(
    room_name: str,
    chat_room_service: ChatRoomService = Depends(get_chat_room_service),
    current_user_id: str = Depends(get_current_user_id),
    ):
    message_history = chat_room_service.get_message_history(
        room_name=room_name,
        user_id=current_user_id
        )
    return message_history


########################################################################################## patch ##########################################################################################

@router.patch('/change_room_setting', status_code=status.HTTP_200_OK)
async def change_room_setting(
    request: ChangeRoomSetting,    
    chat_room_service: ChatRoomService = Depends(get_chat_room_service),
    current_user_id: str = Depends(get_current_user_id)
    ):
    print(request.cur_room_name, request.room_name, request.tag, request.maximum_people)
    chat_room_service.change_room_setting(
        cur_room_name=request.cur_room_name,
        room_name=request.room_name,
        tag=request.tag,
        maximum_people=request.maximum_people
    )