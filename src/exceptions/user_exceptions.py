from fastapi import status

from src.exceptions.base_exceptions import BaseCustomException


class UnregisteredUserError(BaseCustomException):
    def __init__(self, user_name: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{user_name} is an unregistered user."
        )
        

class DuplicateUserIdError(BaseCustomException):
    def __init__(self, user_name: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{user_name} is a duplicate user ID."
        )


class PasswordNotMatchError(BaseCustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match."
        )
        

class MaximumOwnedRoomsExceed(BaseCustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have exceeded the number of rooms you can own."
        )