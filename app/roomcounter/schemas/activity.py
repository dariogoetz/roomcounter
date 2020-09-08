from pydantic import BaseModel
from roomcounter.schemas.room import Room


class PassDoor(BaseModel):
    door_id: int
    left_to_right: bool

    class Config:
        orm_mode = True
