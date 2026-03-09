import threading
import uvicorn
from fastapi import FastAPI
from loguru import logger
from routing.client_routes import router as client_router
from routing.registration import router as reg_router
from storage.connect import create_db_and_tables

class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.app = FastAPI()
        self.logger = logger
        self.logger.add(
            "logs/server_{time:YYYY-MM-DD}.log",
            rotation="10 MB",
            retention="7 days",
            level="INFO",
            enqueue=True
        )

        self.app.include_router(client_router)
        self.app.include_router(reg_router)

        create_db_and_tables()
        self.logger.info(f"Starting server on https://{self.ip}:{self.port}")

        threading.Thread(target=self._run_uvicorn, daemon=True).start()

    def _run_uvicorn(self):
        uvicorn.run(
            self.app,
            host=self.ip,
            port=self.port,
            ssl_certfile="cert.pem",
            ssl_keyfile="key.pem",
            log_level="info"
        )