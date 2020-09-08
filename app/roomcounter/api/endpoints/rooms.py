# -*- coding: utf-8 -*-
"""
    Copyright (c) 2020 Dario Götz.
    All rights reserved.
"""
from fastapi import APIRouter, Depends, HTTPException, status

from typing import List

from sqlalchemy.orm import Session

from roomcounter.api.dependencies import db
from roomcounter.schemas.room import Room, RoomCreate
from roomcounter.crud import crud_room


router = APIRouter()


@router.get("/rooms/", response_model=List[Room])
async def get_rooms(db: Session = Depends(db)):
    return crud_room.get_rooms(db)


@router.post("/rooms/", response_model=Room)
async def add_room(room: RoomCreate, db: Session = Depends(db)):
    room = crud_room.add_room(db, room)
    return room
