from datetime import datetime

from sqlalchemy import Column, String, Integer
from sqlalchemy.sql.sqltypes import DateTime

import sys
sys.path.append('.')

from src.infrastructure.database import Base


class User(Base):
    __tablename__ = "user"
    
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(50), nullable=False)
    password = Column(String(150), nullable=False)
    owned_rooms = Column(Integer, nullable=True, default=0)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
