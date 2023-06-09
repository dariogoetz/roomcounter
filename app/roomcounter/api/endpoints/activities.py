# -*- coding: utf-8 -*-
"""
    Copyright (c) 2020 Dario Götz.
    All rights reserved.
"""
from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from roomcounter.api.dependencies import db, authenticated_user
from roomcounter.crud import crud_activity
from roomcounter.schemas.activity import PassDoor
from roomcounter.schemas.user import AuthenticatedUser
from roomcounter.api.endpoints.websockets import manager


router = APIRouter()


@router.post("/pass_door", response_model=PassDoor)
async def pass_door(
        activity: PassDoor,
        db: Session = Depends(db),
        user: AuthenticatedUser = Depends(authenticated_user)):
    crud_activity.pass_door(db, activity)
    await manager.broadcast("pass_door")
    return activity
