# -*- coding: utf-8 -*-
"""
    Copyright (c) 2020 Dario Götz.
    All rights reserved.
"""
from fastapi import APIRouter, Depends, HTTPException, status

from typing import List

from sqlalchemy.orm import Session

from roomcounter.api.dependencies import db, authenticated_user, admin
from roomcounter.crud import crud_door
from roomcounter.schemas.door import Door, DoorCreate
from roomcounter.schemas.user import AuthenticatedUser


router = APIRouter()


@router.get("/", response_model=List[Door])
async def get_doors(
        db: Session = Depends(db),
        user: AuthenticatedUser = Depends(authenticated_user)):
    doors = crud_door.get_doors(db)
    return doors


@router.get("/{door_id}", response_model=Door)
async def get_door(
        door_id: int, db: Session = Depends(db),
        user: AuthenticatedUser = Depends(authenticated_user)):
    door = crud_door.get_door_by_id(db, door_id)
    return door


@router.post("/", response_model=DoorCreate)
async def add_door(
        door: DoorCreate, db: Session = Depends(db),
        user: AuthenticatedUser = Depends(admin)):
    door = crud_door.add_door(db, door)
    return door


@router.put("/{door_id}", response_model=DoorCreate)
async def put_door(
        door_id: int, door: DoorCreate, db: Session = Depends(db),
        user: AuthenticatedUser = Depends(admin)):
    door = crud_door.add_door(db, door, door_id, put=True)
    return door
