from sqlalchemy.orm import Session
from typing import List, Optional

from roomcounter.models.room import Room
from roomcounter.schemas import room as schema_room

import logging
log = logging.getLogger(__name__)


def get_rooms(db: Session):
    rooms = db.query(Room).all()
    return rooms


def get_room_by_id(db: Session, room_id: int):
    room = db.query(Room).filter(Room.id == room_id).first()
    return room


def add_room(db: Session,
             room: schema_room.RoomCreate,
             room_id: Optional[int] = None,
             put: bool = False):

    if room_id is not None:
        db_room = get_room_by_id(db, room_id)
        if put:
            db_room.name = None
            db_room.capacity = None
    else:
        db_room = Room()

    for key, val in room.dict().items():
        if val is None:
            continue
        setattr(db_room, key, val)

    db_room.utilization = 0

    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room
