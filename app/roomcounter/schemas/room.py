from pydantic import BaseModel


class RoomCreate(BaseModel):
    name: str
    capacity: int

    class Config:
        orm_mode = True


class Room(RoomCreate):
    id: int
    utilization: int
