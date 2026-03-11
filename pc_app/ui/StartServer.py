import uvicorn
from Server.server import app


class Server:
    def __init__(self, ip,port):
        self.port = port
        self.ip = ip
        self.runUvicorn()
    def runUvicorn(self):
        uvicorn.run(app, host=self.ip, port=self.port,ws="websockets")