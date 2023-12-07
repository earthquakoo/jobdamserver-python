from fastapi import Depends
from sqlalchemy.orm import Session

from src.config import load_config
from src.infrastructure.database import get_db
from src.application.user.service import UserService, UserRepository
from src.application.auth.service import AuthService

cfg = load_config()


def get_user_service(session: Session = Depends(get_db)):
    user_repository = UserRepository(session=session)
    auth_service = AuthService(jwt_config=cfg.jwt)
    return UserService(user_repository=user_repository, auth_service=auth_service)
