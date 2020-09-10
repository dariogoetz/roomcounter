from pydantic import BaseModel
from roomcounter.schemas.room import Room


class PassDoor(BaseModel):
    door_id: int
    count_left_to_right: int

    class Config:
        orm_mode = True
