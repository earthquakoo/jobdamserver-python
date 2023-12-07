from fastapi import status

from src.exceptions.base_exceptions import BaseCustomException


class UnregisteredUserError(BaseCustomException):
    def __init__(self, user_name: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{user_name} is an unregistered user."
        )
        

class DuplicateRoomNameError(BaseCustomException):
    def __init__(self, room_name: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{room_name} is a duplicate room name."
        )

        
class PersonnelOvercountError(BaseCustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot set it smaller than the number of people in the current room."
        )