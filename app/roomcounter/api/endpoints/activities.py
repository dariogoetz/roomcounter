# -*- coding: utf-8 -*-
"""
    Copyright (c) 2020 Dario Götz.
    All rights reserved.
"""
from fastapi import APIRouter, Depends, HTTPException, status

from typing import List

from sqlalchemy.orm import Session

from roomcounter.api.dependencies import db
from roomcounter.crud import crud_activity
from roomcounter.schemas.activity import PassDoor


router = APIRouter()


@router.post("/pass_door/", response_model=PassDoor)
async def pass_door(activity: PassDoor, db: Session = Depends(db)):
    res = crud_activity.pass_door(db, activity)
    return res
