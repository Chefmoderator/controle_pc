from fastapi import FastAPI, Header, HTTPException
from auth import check_key, generate_key

from core.system_control import InfoManager,PowerManagement,LaunchProgram,LaunchProgram,RemoteVolume,ScreenBrightnessControl
from core.processes import ProcessManger
from core.file_manager import FileManager

app = FastAPI()

SERVER_KEY = generate_key()

def auth_key(key: str):
    if key is None or not check_key(key):
        raise HTTPException(status_code=401, detail="Invalid API key")

@app.get("/info/system")
def system_info(x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return InfoManager.info_manager_json()

@app.get("/power/shutdown")
def shutdown(x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    PowerManagement.shutdown()
    return {"status": "ok"}

@app.get("/power/restart")
def shutdown(x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    PowerManagement.restart()
    return {"status": "ok"}

@app.get("/power/sleep")
def shutdown(x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    PowerManagement.sleep()
    return {"status": "ok"}

@app.get("/power/hibernate")
def shutdown(x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    PowerManagement.hibernate()
    return {"status": "ok"}

@app.get("/volume/mute")
def mute(x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    RemoteVolume.mute()
    return {"status": "ok"}

@app.get("/volume/unmute")
def mute(x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    RemoteVolume.unmute()
    return {"status": "ok"}

@app.get("/volume/set/{value}")
def mute(value: int, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    RemoteVolume.set_volume(value)
    return {"status": "ok"}

@app.get("/volume/get")
def mute(x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {"volume": RemoteVolume.get_volume()}

@app.get("/brightness/get")
def mute(x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {"brightness": ScreenBrightnessControl.get_brightness()}

@app.get("/brightness/set/{value}")
def mute(value:int ,x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    ScreenBrightnessControl.set_brightness(value)
    return {"status": "ok"}

@app.get("/program/launch/{value}")
def launch_program(value: str, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    LaunchProgram.launch_program(value)
    return {"status":"ok"}



