class UserEntity:
    def __init__(self, user_name: str, password: str, user_id: int = None):
        self.user_name = user_name
        self.password = password
        self.user_id = user_id

    def assign_user_id(self, user_id: int) -> None:
        self.user_id = user_id
    
