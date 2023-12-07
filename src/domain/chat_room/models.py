from datetime import datetime

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime

import sys
sys.path.append('.')

from src.infrastructure.database import Base


class ChatRoom(Base):
    __tablename__ = "room"
    
    room_id = Column(Integer, primary_key=True, autoincrement=True)
    room_name = Column(String(50), nullable=False)
    tag = Column(String(50), nullable=False)
    personnel = Column(Integer, nullable=False)
    maximum_people = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    room_members = relationship("RoomMember", back_populates="rooms", cascade="all, delete-orphan")
    room_messages = relationship("Message", back_populates="messages", cascade="all, delete-orphan")

    
class RoomMember(Base):
    __tablename__ = "room_member"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    room_name = Column(String(50), nullable=False)
    room_id = Column(Integer, ForeignKey("room.room_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    connection_id = Column(String(100), nullable=True)
    joined_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    rooms = relationship("ChatRoom", back_populates="room_members")
    
    
class Message(Base):
    __tablename__ = "message"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(500), nullable=False)
    room_id = Column(Integer, ForeignKey("room.room_id"), nullable=False)
    user_name = Column(String(50), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    messages = relationship("ChatRoom", back_populates="room_messages")