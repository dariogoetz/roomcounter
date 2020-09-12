# -*- coding: utf-8 -*-
"""
    Copyright (c) 2020 Dario Götz.
    All rights reserved.
"""
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse, Response
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session


from roomcounter.api.dependencies import db, optional_user
from roomcounter.core import security
from roomcounter.core.config import settings
from roomcounter.crud import crud_user
from roomcounter.schemas.user import AuthenticatedUser


router = APIRouter()


@router.post("/login")
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(db),
):
    user = crud_user.verify_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token_expires = timedelta(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={
            "sub": user.username,
            "permissions": [p.permission for p in user.permissions],
            "id": user.id
        },
        expires_delta=access_token_expires
    )
    # return {"access_token": access_token, "token_type": "bearer"}

    # the following is used for the OAuth2PasswordBearerCookie workflow
    # that uses cookies instead of Authentication Headers
    # if came_from:
    # response = RedirectResponse(came_from,
    #                             status_code=status.HTTP_303_SEE_OTHER)
    # else:
    response = JSONResponse({"access_token": access_token,
                             "token_type": "bearer"})

    response.set_cookie(
        "Authorization",
        value=f"Bearer {access_token}",
        httponly=True,
        # max_age=1800,
        # expires=1800,
    )
    return response


@router.get("/logout")
async def route_logout_and_remove_cookie(response: Response):
    response.delete_cookie("Authorization")


@router.get("/me", response_model=AuthenticatedUser)
async def me(current_user: AuthenticatedUser = Depends(optional_user)):
    return current_user
