from pydantic import BaseModel
from roomcounter.schemas.room import Room


class DoorBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class DoorCreate(DoorBase):
    left_room_id: int
    right_room_id: int


class DoorUpdate(DoorCreate):
    id: int


class Door(DoorCreate):
    id: int
    left_room: Room
    right_room: Room
