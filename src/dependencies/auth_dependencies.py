from jose import ExpiredSignatureError
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from src.config import load_config
from src.application.auth.service import AuthService
from src.exceptions.auth_exceptions import JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", scheme_name="JWT")

cfg = load_config()

auth_handler = AuthService(jwt_config=cfg.jwt)


def get_current_user_id(token: str = Depends(oauth2_scheme)):
    try:
        user_id = auth_handler.decode_access_token(token)
        return user_id
    except ExpiredSignatureError:
        raise JWTError()


def get_token(token: str = Depends(oauth2_scheme)):
    return token
