from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt, ExpiredSignatureError

from src.config import JWTConfig
from src.exceptions.auth_exceptions import (
    InvalidTokenError,
    ExpiredTokenError,
)


class AuthService:
    def __init__(self, jwt_config: JWTConfig):
        self.jwt_config = jwt_config
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_data(self, raw: str):
        return self.pwd_context.hash(raw)


    def verify_data(self, raw: str, hashed: str):
        return self.pwd_context.verify(raw, hashed)


    def create_access_token(self, data: str):
        payload = {
            "sub": str(data),
            "scope": "access_token",
            "exp": datetime.utcnow() + timedelta(minutes=self.jwt_config.ACCESS_TOKEN_EXPIRE_MINUTES),
            "iat": datetime.utcnow(),
        }
        return jwt.encode(payload, self.jwt_config.SECRET_KEY, algorithm=self.jwt_config.ALGORITHM)


    def create_refresh_token(self, data: str):
        payload = {
            "sub": str(data),
            "scope": "access_token",
            "exp": datetime.utcnow() + timedelta(minutes=self.jwt_config.REFRESH_TOKEN_EXPIRE_MINUTES),
            "iat": datetime.utcnow(),
        }
        return jwt.encode(payload, self.jwt_config.SECRET_KEY, algorithm=self.jwt_config.ALGORITHM)


    def decode_access_token(self, token: str):
        try:
            payload = jwt.decode(token, self.jwt_config.SECRET_KEY, algorithms=[self.jwt_config.ALGORITHM])
            if payload["scope"] != "access_token":
                raise InvalidTokenError()
            user_id = payload['sub']
            return user_id
        except ExpiredSignatureError:
            raise ExpiredTokenError()
            
        
    def decode_refresh_jwt(self, token: str):
        try:
            payload = jwt.decode(token, self.jwt_config.SECRET_KEY, algorithms=[self.jwt_config.ALGORITHM])
            if payload["scope"] != "refresh_token":
                raise InvalidTokenError
            user_id = payload['sub']
            return user_id
        except ExpiredSignatureError:
            raise ExpiredTokenError()