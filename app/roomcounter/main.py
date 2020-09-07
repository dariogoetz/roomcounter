from fastapi import FastAPI, Depends

from roomcounter.api.api import api_router
from roomcounter.core.config import settings
from roomcounter.api.dependencies import admin
from roomcounter.schemas.user import AuthenticatedUser
from roomcounter.db.init_db import init_database

app = FastAPI(title=settings.APP_NAME)

app.include_router(api_router)


init_database()


@app.get("/users/me", response_model=AuthenticatedUser)
async def me(current_user: AuthenticatedUser = Depends(admin)):
    return current_user
