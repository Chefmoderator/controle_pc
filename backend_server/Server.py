import threading
import uvicorn
from fastapi import FastAPI
from loguru import logger
from routing.client_routes import router as client_router
from storage.connect import create_db_and_tables
from UI.LogWindow import LogWindow
import logging

class LogHandler(logging.Handler):

    def __init__(self, log_window):
        super().__init__()
        self.log_window = log_window

    def emit(self, record):
        msg = self.format(record) + "\n"
        self.log_window.write(msg)

class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port


        self.log_window = LogWindow()


        logger.remove()
        logger.add(
            self.log_window.write_from_loguru,
            format="{time:HH:mm:ss} | {level} | {message}",
            level="INFO"
        )

        logger.add(
            "logs/server_{time:YYYY-MM-DD}.log",
            rotation="10 MB",
            retention="7 days",
            level="INFO",
            enqueue=True
        )

        handler = LogHandler(self.log_window)
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s')
        handler.setFormatter(formatter)

        root_logger = logging.getLogger()
        root_logger.handlers = []
        root_logger.addHandler(handler)
        root_logger.setLevel(logging.INFO)

        sqlalchemy_logger = logging.getLogger("sqlalchemy.engine")
        sqlalchemy_logger.handlers = []
        sqlalchemy_logger.propagate = False
        sqlalchemy_logger.addHandler(handler)
        sqlalchemy_logger.setLevel(logging.INFO)

        uvicorn_logger = logging.getLogger("uvicorn")
        uvicorn_logger.handlers = []
        uvicorn_logger.propagate = False
        uvicorn_logger.addHandler(handler)
        uvicorn_logger.setLevel(logging.INFO)

        uvicorn_access_logger = logging.getLogger("uvicorn.access")
        uvicorn_access_logger.handlers = []
        uvicorn_access_logger.propagate = False
        uvicorn_access_logger.addHandler(handler)
        uvicorn_access_logger.setLevel(logging.INFO)

        self.app = FastAPI()
        self.app.include_router(client_router)

        create_db_and_tables()
        logger.info(f"Starting server at http://{self.ip}:{self.port}")


        threading.Thread(target=self.runUvicorn, daemon=True).start()

        self.log_window.start()

    def runUvicorn(self):
        uvicorn.run(
            self.app,
            host=self.ip,
            port=self.port,
            log_level="info"
        )