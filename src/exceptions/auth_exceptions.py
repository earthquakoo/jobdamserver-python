from fastapi import status

from src.exceptions.base_exceptions import BaseCustomException

        
class InvalidTokenError(BaseCustomException):
    def __init__(self):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = "Invalid token"
        

class ExpiredTokenError(BaseCustomException):
    def __init__(self):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = "Expired signature token"
        
        
class JWTError(BaseCustomException):
    def __init__(self):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = "JWT error"