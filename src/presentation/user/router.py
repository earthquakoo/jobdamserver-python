from fastapi import APIRouter, status, Depends

import sys
sys.path.append('.')

from src.application.user.service import UserService
from src.dependencies.user_dependencies import get_user_service
from src.dependencies.auth_dependencies import get_current_user_id
from src.presentation.user.dtos import (
    RegisterRequest, RegisterResponse,
    LoginRequest, LoginResponse,
)



router = APIRouter(
    prefix="/user",
    tags=["user"]  
)


@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=RegisterResponse)
async def register(data: RegisterRequest, user_service: UserService = Depends(get_user_service)):
    
    new_user_entity = user_service.register_user(user_name=data.user_name, password=data.password)

    return RegisterResponse(user_name=new_user_entity.user_name)


@router.post('/login', status_code=status.HTTP_200_OK, response_model=LoginResponse)
def login(data: LoginRequest, user_service: UserService = Depends(get_user_service)):
    
    login_response = user_service.login_user(user_name=data.user_name, password=data.password)

    return LoginResponse(
        user_id=login_response.user_id,
        user_name=login_response.user_name,
        access_token=login_response.access_token,
        refresh_token=login_response.refresh_token
        )
    
    
@router.get("/validate-access-token", status_code=status.HTTP_200_OK)
async def validate_jwt(current_user_id: str = Depends(get_current_user_id)):
    return {"detail": "validated"}