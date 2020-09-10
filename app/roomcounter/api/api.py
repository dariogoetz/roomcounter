from fastapi import APIRouter

from roomcounter.api.endpoints import login, rooms, doors, activities

api_router = APIRouter()
api_router.include_router(login.router, prefix="/auth", tags=["login"])
api_router.include_router(rooms.router, prefix="/room", tags=["room"])
api_router.include_router(doors.router, prefix="/door", tags=["door"])
api_router.include_router(activities.router, prefix="/activity", tags=["activity"])
