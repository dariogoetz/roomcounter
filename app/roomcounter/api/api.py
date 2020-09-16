from fastapi import APIRouter

from roomcounter.api.endpoints import login, rooms, doors, activities, websockets

api_router = APIRouter()
api_router.include_router(login.router, prefix="/auth", tags=["login"])
api_router.include_router(websockets.router, prefix="/websockets", tags=["websockets"])
api_router.include_router(rooms.router, prefix="/rooms", tags=["room"])
api_router.include_router(doors.router, prefix="/doors", tags=["door"])
api_router.include_router(activities.router, prefix="/activities", tags=["activity"])
