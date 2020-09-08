from sqlalchemy.orm import Session
from typing import List, Optional

from roomcounter.models.room import Door
from roomcounter.schemas import activity as schema_activity


def pass_door(db: Session, activity: schema_activity.PassDoor):
    door = db.query(Door).filter(Door.id == activity.door_id).first()

    if activity.left_to_right:
        left_increment = -1
    else:
        left_increment = 1

    if door.left_room.capacity != 0:
        door.left_room.utilization += left_increment
    if door.right_room.capacity != 0:
        door.right_room.utilization -= left_increment
    return activity
