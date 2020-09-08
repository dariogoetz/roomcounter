# -*- coding: utf-8 -*-
"""
    Copyright (c) 2020 Dario Götz.
    All rights reserved.
"""
from fastapi import APIRouter, Depends, HTTPException, status

from typing import List

from sqlalchemy.orm import Session

from roomcounter.api.dependencies import db
from roomcounter.crud import crud_door
from roomcounter.schemas.door import Door, DoorCreate


router = APIRouter()


@router.get("/doors/", response_model=List[Door])
async def get_doors(db: Session = Depends(db)):
    doors = crud_door.get_doors(db)
    return doors


@router.post("/doors/", response_model=DoorCreate)
async def add_door(door: DoorCreate, db: Session = Depends(db)):
    door = crud_door.add_door(db, door)
    return door


@router.put("/doors/{door_id}", response_model=DoorCreate)
async def put_door(door: DoorCreate, db: Session = Depends(db)):
    door = crud_door.add_door(db, door)
    return door
