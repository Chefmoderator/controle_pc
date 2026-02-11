from fastapi import FastAPI, WebSocket
from loguru import logger
from routing.pc_routes import router as pc_router
from routing.client_routes import router as client_router
from routing.ws_manager import handle_pc_connection
from routing.ws_users import handle_user_connection
import ssl
import uvicorn

app = FastAPI()

logger.add(
    "logs/server_{time:YYYY-MM-DD}.log",
    rotation="10 MB",
    retention="7 days",
    level="INFO",
    enqueue=True
)

app.include_router(pc_router)
app.include_router(client_router)

@app.websocket("/ws/pc/{pc_id}")
async def pc_ws(ws: WebSocket, pc_id: str, token: str):
    logger.info(f"[WS-PC] Incoming connection from PC {pc_id}, IP: {ws.client.host}")
    await handle_pc_connection(pc_id, token, ws)

@app.websocket("/ws/user/{pc_id}")
async def user_ws(ws: WebSocket, pc_id: str, token: str):
    logger.info(f"[WS-USER] Incoming connection for PC {pc_id}, IP: {ws.client.host}")
    await handle_user_connection(pc_id, token, ws)

if __name__ == "__main__":
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

    logger.info("Starting server on https://0.0.0.0:8443")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8443,
        ssl_certfile="cert.pem",
        ssl_keyfile="key.pem",
        log_level="info"
    )

