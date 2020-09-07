from fastapi import APIRouter

from roomcounter.api.endpoints import login

api_router = APIRouter()
api_router.include_router(login.router, prefix="/auth", tags=["login"])
