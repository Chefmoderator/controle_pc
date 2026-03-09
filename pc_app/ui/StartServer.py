import uvicorn

class Server:
    def __init__(self, ip,port):
        self.port = port
        self.ip = ip
        self.runUvicorn()

    def runUvicorn(self):
        uvicorn.run("Server.server:app", host=self.ip, port=self.port)
