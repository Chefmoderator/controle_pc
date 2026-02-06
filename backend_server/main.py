from fastapi import FastAPI, WebSocket
from routing.pc_routes import router as pc_router
from routing.client_routes import router as client_router
from routing.ws_manager import handle_pc_connection

app = FastAPI()

app.include_router(pc_router)
app.include_router(client_router)

@app.websocket("/ws/pc/{pc_id}")
async def pc_websocket(ws: WebSocket, pc_id: str):
    await handle_pc_connection(pc_id, ws)
