from sqlalchemy.orm import Session
from typing import List, Optional

from roomcounter.models.room import Door, Room
from roomcounter.schemas import door as schema_door


def get_doors(db: Session):
    doors = db.query(Door).all()
    return doors


def get_door_by_id(db: Session, door_id: int):
    door = db.query(Door).filter(Door.id == door_id).first()
    return door


def add_door(db: Session,
             door: schema_door.DoorCreate,
             door_id: Optional[int] = None,
             put: bool = False):
    left_room = db.query(Room).filter(Room.id == door.left_room_id).first()
    right_room = db.query(Room).filter(Room.id == door.right_room_id).first()

    assert left_room is not None
    assert right_room is not None

    if door_id is not None:
        db_door = get_door_by_id(db, door_id)
        if put:
            db_door.name = None
            db_door.left_room_id = None
            db_door.right_room_id = None
    else:
        db_door = Door()

    for key, val in door.dict().items():
        if val is None:
            continue
        setattr(db_door, key, val)

    db.add(db_door)
    db.commit()
    db.refresh(db_door)
    return db_door
