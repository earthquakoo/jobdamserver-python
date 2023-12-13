from sqlalchemy.orm import Session
from src.utils.general_utils import sql_obj_list_to_dict_list, sql_obj_to_dict
from src.domain.chat_room.models import (
    ChatRoom,
    RoomMember,
    Message
)
from src.exceptions.chat_room_exceptions import (
    PersonnelOvercountError,
    DuplicateRoomNameError
)
from src.exceptions.user_exceptions import MaximumOwnedRoomsExceed
from src.domain.user.models import User
from src.domain.chat_room.entities import (
    ChatRoomEntity
)


class ChatRoomRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def create_room(self, chat_room_entity: ChatRoomEntity) -> ChatRoomEntity:
        existing_room = self.session.query(ChatRoom).filter(ChatRoom.room_name==chat_room_entity.room_name).first()
        if existing_room:
            raise DuplicateRoomNameError(room_name=chat_room_entity.room_name)
        
        new_chat_room_entity = ChatRoom(
            room_name=chat_room_entity.room_name,
            tag=chat_room_entity.tag,
            personnel=chat_room_entity.personnel,
            maximum_people=chat_room_entity.maximum_people,
            user_id=chat_room_entity.user_id
            )
        
        user_info = self.session.query(User).filter(User.user_id==chat_room_entity.user_id).first()
        
        if user_info.owned_rooms >= 3:
            raise MaximumOwnedRoomsExceed()
        
        user_info.owned_rooms += 1
        
        self.session.add(new_chat_room_entity)
        self.session.commit()
        self.session.refresh(new_chat_room_entity)
        chat_room_entity.assign_room_id(room_id=new_chat_room_entity.room_id)
        
        return chat_room_entity
        
        
    def save_message(self, room_name: str, user_name: str, content: str):
        room_id = self.session.query(ChatRoom).filter(ChatRoom.room_name==room_name).first().room_id
        new_message_entity = Message(
            room_id=room_id,
            user_name=user_name,
            content=content
            )
        
        self.session.add(new_message_entity)
        self.session.commit()
        self.session.refresh(new_message_entity)
        
        
    def delete_room(self, room_name: str, user_id: int):
        room = self.session.query(ChatRoom).filter(ChatRoom.room_name==room_name).first()
        user_info = self.session.query(User).filter(User.user_id==user_id).first()
        
        user_info.owned_rooms -= 1
        
        self.session.delete(room)
        self.session.commit()
    

    def join_room(self, user_id: int, room_name: str):
        member = self.session.query(RoomMember).filter(
            RoomMember.user_id==user_id,
            RoomMember.room_name==room_name,
            ).first()
        
        if member:
            return None
        
        room = self.session.query(ChatRoom).filter(ChatRoom.room_name==room_name).first()
        room.personnel += 1
                
        new_member = RoomMember(
            room_name=room_name,
            user_id=user_id,
            room_id=room.room_id,
        )
        
        self.session.add(new_member)
        self.session.commit()
        self.session.refresh(new_member)
    
    
    def leave_room(self, room_name: str, user_name: str | None, user_id: int | None):
        join_room = self.session.query(ChatRoom).filter(ChatRoom.room_name==room_name).first()
        if user_name:
            user_id = self.session.query(User).filter(User.user_name==user_name).first().user_id
            
        leave_room = self.session.query(RoomMember).filter(
            RoomMember.room_name==room_name,
            RoomMember.user_id==user_id,
            ).first()
        
        join_room.personnel -= 1
        
        self.session.delete(leave_room)
        self.session.commit()        
    
    
    def get_current_room_member_list(self, room_name: str) -> list:
        room_members = self.session.query(RoomMember).filter(RoomMember.room_name==room_name).all()
        
        room_members_dict_list = sql_obj_list_to_dict_list(room_members)
        room_members_list = []
        
        for i in range(len(room_members_dict_list)):
            user_id = self.session.query(RoomMember).filter(RoomMember.user_id==room_members_dict_list[i]['user_id']).first().user_id
            user_name = self.session.query(User).filter(User.user_id==user_id).first().user_name
            room_members_list.append(user_name)

        return room_members_list
    
    
    def get_joined_rooms_list(self, user_id: int) -> list:
        joined_rooms_list = self.session.query(RoomMember).filter(RoomMember.user_id==user_id).all()
        
        if joined_rooms_list is None:
            return None
        
        room_dict_list = sql_obj_list_to_dict_list(joined_rooms_list)
        room_list = []
        
        for i in range(len(room_dict_list)):
            room = self.session.query(ChatRoom).filter(ChatRoom.room_id==room_dict_list[i]['room_id']).first()
            room_list.append(sql_obj_to_dict(room))
        
        return room_list
    
    
    def get_all_rooms_list(self) -> list:
        all_room_list = self.session.query(ChatRoom).order_by(ChatRoom.room_id.desc()).all()
        all_room_dict_list = sql_obj_list_to_dict_list(all_room_list)
        
        return all_room_dict_list
    
    
    def get_rooms_list(self, room_name: str | None, tag: str | None) -> list:
        if room_name:
            all_rooms_list = sql_obj_list_to_dict_list(self.session.query(ChatRoom).all())
            matched_room = []
            
            for i in range(len(all_rooms_list)):
                room_info = all_rooms_list[i]['room_name']
                if room_name in room_info:
                    room = self.session.query(ChatRoom).filter(ChatRoom.room_name==all_rooms_list[i]['room_name']).first()
                    matched_room.append(sql_obj_to_dict(room))
        
        if tag:
            all_rooms_list = self.session.query(ChatRoom).filter(ChatRoom.tag==tag).all()
            matched_room = sql_obj_list_to_dict_list(all_rooms_list)
        
        return matched_room
    
    
    def get_message_history(self, room_name: str, user_id: int):
        room_id = self.session.query(ChatRoom).filter(ChatRoom.room_name==room_name).first().room_id
        joined_at = self.session.query(RoomMember).filter(RoomMember.user_id==user_id).first().joined_at
        message_history = self.session.query(Message).filter(
            Message.room_id==room_id,
            Message.created_at>joined_at
        ).all()
        
        return sql_obj_list_to_dict_list(message_history)
    
    
    def change_room_setting(self, cur_room_name: str, room_name: str, tag: str, maximum_people: int) -> None:
        chat_room_obj = self.session.query(ChatRoom).filter(ChatRoom.room_name==cur_room_name).first()
        
        if room_name:
            new_room = self.session.query(ChatRoom).filter(ChatRoom.room_name==room_name).first()
            if new_room:
                raise DuplicateRoomNameError(room_name=room_name)
            chat_room_obj.room_name = room_name
            room_member_obj = self.session.query(RoomMember).filter(RoomMember.room_name==cur_room_name).first()
            room_member_obj.room_name = room_name
        if tag:
            chat_room_obj.tag = tag
        if maximum_people:
            if chat_room_obj.personnel > maximum_people:
                raise PersonnelOvercountError()
            chat_room_obj.maximum_people = maximum_people
        
        self.session.commit()