from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from roomcounter.core.websockets import manager

router = APIRouter()


@router.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect(websocket)
