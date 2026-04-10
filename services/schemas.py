from pydantic import BaseModel


class RoomRequest(BaseModel):
    room_name: str
    password: str
    username: str
    