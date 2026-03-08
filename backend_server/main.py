from fastapi import FastAPI, WebSocket
from loguru import logger
from routing.pc_routes import router as pc_router
from routing.client_routes import router as client_router
from routing.registration import router as reg_router
from storage.connect import create_db_and_tables
import ssl
import uvicorn
import requests

def get_ip():
    try:
        response = requests.get('https://api.ipify.org')
        return response.text
    except Exception as e:
        return str(e)

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
app.include_router(reg_router)

if __name__ == "__main__":
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
    create_db_and_tables()

    ip = get_ip()
    logger.info("Starting server on https://0.0.0.0:8443")
    uvicorn.run("main:app", host="0.0.0.0", port=8443, log_level="info")

