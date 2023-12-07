from src.application.user.repositories import UserRepository
from src.application.auth.service import AuthService
from src.exceptions.user_exceptions import (
    UnregisteredUserError,
    DuplicateUserIdError,
    PasswordNotMatchError,
)
from src.domain.user.entities import UserEntity
from src.application.user.dtos import (
    LoginServiceResponse,
)


class UserService:
    def __init__(self, user_repository: UserRepository, auth_service: AuthService):
        self.user_repository = user_repository
        self.auth_service = auth_service
        
    
    def register_user(self, user_name: str, password: str):
        
        user_info = self.user_repository.get_user_by_user_name(user_name=user_name)
        if user_info is not None:
            raise DuplicateUserIdError(user_name=user_name)
        
        hashed_password = self.auth_service.hash_data(raw=password)

        user_entity = UserEntity(user_name=user_name, password=hashed_password)
        new_user_entity = self.user_repository.create_user(user_entity=user_entity)

        return new_user_entity


    def login_user(self, user_name: str, password: str):
        user_info = self.user_repository.get_user_by_user_name(user_name)
        
        if user_info is None:
            raise UnregisteredUserError(user_name=user_name)
        
        if not self.auth_service.verify_data(raw=password, hashed=user_info.password):
            raise PasswordNotMatchError()
        
        access_token = self.auth_service.create_access_token(user_info.user_id)
        refresh_token = self.auth_service.create_refresh_token(user_info.user_id)
        
        return LoginServiceResponse(
            user_id=user_info.user_id,
            user_name=user_name,
            access_token=access_token,
            refresh_token=refresh_token
            )