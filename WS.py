from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
from DataJobs import runningJobs

ws_router=APIRouter()

async def websocket_endpoint(websocket: WebSocket):

    while True:
        if not runningJobs==[]:
            temp=runningJobs.pop()
            await websocket.send_text(f"{temp.Name} is running")        

@ws_router.websocket("/ws")
async def websocket_end(ws:WebSocket):
    await ws.accept()
    try:
        await asyncio.gather(
        websocket_endpoint(ws),
    )
    except WebSocketDisconnect:
        ws.disconnect()
        print("Client Disconnected")
