from fastapi import Depends
from sqlalchemy.orm import Session

from src.application.chat_room.repositories import ChatRoomRepository
from src.application.chat_room.service import ChatRoomService
from src.application.auth.service import AuthService
from src.infrastructure.database import get_db
from src.config import load_config

cfg = load_config()

def get_chat_room_service(session: Session = Depends(get_db)):
    repository = ChatRoomRepository(session=session)
    return ChatRoomService(chat_room_repository=repository)