from typing import Union
from pydantic import BaseModel
from datetime import datetime


class RegisterRequest(BaseModel):
    user_name: str
    password: str


class RegisterResponse(BaseModel):
    user_name: str


class LoginRequest(BaseModel):
    user_name: str
    password: str
    
    
class LoginResponse(BaseModel):
    user_id: int
    user_name: str
    access_token: str
    refresh_token: str