from sqlalchemy.orm import Session
from typing import List, Optional

from roomcounter.models.room import Door
from roomcounter.schemas import activity as schema_activity


def pass_door(db: Session, activity: schema_activity.PassDoor):
    door = db.query(Door).filter(Door.id == activity.door_id).first()
    if door.left_room.capacity != 0:
        door.left_room.utilization -= activity.count_left_to_right
    if door.right_room.capacity != 0:
        door.right_room.utilization += activity.count_left_to_right
    return activity
