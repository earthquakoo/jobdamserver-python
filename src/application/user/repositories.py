from sqlalchemy.orm import Session

from src.domain.user.models import User
from src.domain.user.entities import (
    UserEntity
)


class UserRepository:
    def __init__(self, session: Session):
        self.session = session
        
    def get_user_by_user_name(self, user_name: str):
        user_info = self.session.query(User).filter(User.user_name==user_name).first()

        if user_info is None:
            return None
        
        return UserEntity(
            user_id=user_info.user_id,
            user_name=user_info.user_name,
            password=user_info.password
        )

    def create_user(self, user_entity: UserEntity):
        new_user_entity = User(user_name=user_entity.user_name, password=user_entity.password)
        
        self.session.add(new_user_entity)
        self.session.commit()
        self.session.refresh(new_user_entity)
        
        return new_user_entity