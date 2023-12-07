class ChatRoomEntity:
    def __init__(self, room_name: str, tag: str, personnel: int, maximum_people: int, user_id: int, room_id: int = None):
        self.room_name = room_name
        self.tag = tag
        self.personnel = personnel
        self.maximum_people = maximum_people
        self.room_id = room_id
        self.user_id = user_id

    def assign_room_id(self, room_id: int) -> None:
        self.room_id = room_id