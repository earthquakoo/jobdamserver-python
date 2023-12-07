from pydantic import BaseModel


class LoginServiceResponse(BaseModel):
    user_id: int
    user_name: str
    access_token: str
    refresh_token: str