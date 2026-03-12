import uvicorn
from Server.server import app
from ui.LogWindow import LogWindow
import threading

class Server:
    def __init__(self, ip, port):
        self.port = port
        self.ip = ip
        self.run()

    def run(self):
        log_window = LogWindow()
        threading.Thread(
            target=lambda: uvicorn.run(app, host=self.ip, port=self.port, ws="websockets"),
            daemon=True
        ).start()

        log_window.start()