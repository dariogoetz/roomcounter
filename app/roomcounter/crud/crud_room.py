from sqlalchemy.orm import Session
from typing import List, Optional

from roomcounter.models.room import Room
from roomcounter.schemas import room as schema_room

import logging
log = logging.getLogger(__name__)


def get_rooms(db: Session):
    rooms = db.query(Room).all()
    return rooms


def add_room(db: Session, room: schema_room.RoomCreate):
    room = Room(**room.dict(), utilization=0)
    db.add(room)
    db.commit()
    db.refresh(room)
    return room
