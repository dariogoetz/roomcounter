# -*- coding: utf-8 -*-
"""
    Copyright (c) 2020 Dario Götz.
    All rights reserved.
"""
from fastapi import APIRouter, Depends

from typing import List

from sqlalchemy.orm import Session

from roomcounter.api.dependencies import db, authenticated_user, admin
from roomcounter.schemas.room import Room, RoomCreate
from roomcounter.crud import crud_room
from roomcounter.schemas.user import AuthenticatedUser


router = APIRouter()


@router.get("/", response_model=List[Room])
async def get_rooms(
        db: Session = Depends(db),
        user: AuthenticatedUser = Depends(authenticated_user)):
    return crud_room.get_rooms(db)


@router.post("/", response_model=Room)
async def add_room(
        room: RoomCreate,
        db: Session = Depends(db),
        user: AuthenticatedUser = Depends(admin)):
    room = crud_room.add_room(db, room)
    return room


@router.put("/{room_id}", response_model=RoomCreate)
async def put_room(
        room_id: int,
        room: RoomCreate,
        db: Session = Depends(db),
        user: AuthenticatedUser = Depends(admin)):
    room = crud_room.add_room(db, room, room_id, put=True)
    return room
