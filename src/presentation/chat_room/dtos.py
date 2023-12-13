from typing import Union
from pydantic import BaseModel
from datetime import datetime


class CreateRoomRequest(BaseModel):
    room_name: str
    tag: str
    maximum_people: int


class CreateRoomResponse(BaseModel):
    room_name: str
    maximum_people: int
    tag: str
    

class RoomNameRequest(BaseModel):
    room_name: str


class SaveMessageRequest(BaseModel):
    user_name: str
    room_name: str
    content: str


class LeaveRoomRequest(BaseModel):
    user_name: str | None = None
    room_name: str


class ChangeRoomSetting(BaseModel):
    cur_room_name: str
    room_name: str | None = None
    maximum_people: int | None = None
    tag: str | None = None