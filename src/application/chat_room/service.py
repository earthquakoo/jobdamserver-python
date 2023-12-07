from src.application.chat_room.repositories import ChatRoomRepository
from src.exceptions.chat_room_exceptions import (
    DuplicateRoomNameError,
    PersonnelOvercountError
)
from src.exceptions.user_exceptions import MaximumOwnedRoomsExceed
from src.domain.chat_room.entities import (
    ChatRoomEntity
)



class ChatRoomService:
    def __init__(self, chat_room_repository: ChatRoomRepository):
        self.chat_room_repository = chat_room_repository

    
    def create_chat_room(self, room_name: str, tag: str, maximum_people: int, user_id: int) -> ChatRoomEntity:
        chat_room_entity = ChatRoomEntity(
            room_name=room_name,
            tag=tag,
            personnel=0,
            maximum_people=maximum_people,
            user_id=user_id
            )
        try:
            new_chat_room_entity = self.chat_room_repository.create_room(chat_room_entity=chat_room_entity)
            
            self.chat_room_repository.join_room(
                user_id=user_id,
                room_name=room_name
            )
    
        except DuplicateRoomNameError:
            raise DuplicateRoomNameError()
        
        except MaximumOwnedRoomsExceed:
            raise MaximumOwnedRoomsExceed()

        return new_chat_room_entity
    
    
    def save_message(self, room_name: str, user_name: str, content: str):
        self.chat_room_repository.save_message(
            room_name=room_name,
            user_name=user_name,
            content=content
            )
    
    
    def delete_room(self, room_name: str, user_id: int) -> None:
        self.chat_room_repository.delete_room(
            room_name=room_name,
            user_id=user_id
            )
    
    
    def join_room(self, room_name: str, user_id: int):
        self.chat_room_repository.join_room(
            room_name=room_name,
            user_id=user_id
        )

    
    def leave_room(self, room_name: str, user_name: str | None, user_id: int | None) -> None:
        self.chat_room_repository.leave_room(
            room_name=room_name,
            user_name=user_name,
            user_id=user_id
            )
    
    
    def get_current_room_member_list(self, room_name: str):
        room_members_list = self.chat_room_repository.get_current_room_member_list(room_name=room_name)
        
        return room_members_list
    
    
    def get_joined_rooms_list(self, user_id: int):
        room_list = self.chat_room_repository.get_joined_rooms_list(user_id=user_id)
        
        return room_list
    
    
    def get_all_rooms_list(self):
        all_rooms_list = self.chat_room_repository.get_all_rooms_list()
        
        return all_rooms_list
    
    
    def get_rooms_list(self, search_word: str) -> list:
        room_name = None
        tag = None
        args = search_word.split()
        if args[0] == "tag":
            tag = args[1]
        else:
            room_name = search_word
            
        rooms_list = self.chat_room_repository.get_rooms_list(room_name=room_name, tag=tag)
        
        return rooms_list
    
    
    def get_message_history(self, room_name: str, user_id: int):
        message_history = self.chat_room_repository.get_message_history(room_name=room_name, user_id=user_id)
        return message_history

    
    def change_room_setting(
        self,
        cur_room_name: str,
        room_name: str | None,
        tag: str | None,
        maximum_people: int | None
        ) -> None:
        try:
            self.chat_room_repository.change_room_setting(
                cur_room_name=cur_room_name,
                room_name=room_name,
                tag=tag,
                maximum_people=maximum_people
            )
        except PersonnelOvercountError:
            raise PersonnelOvercountError()