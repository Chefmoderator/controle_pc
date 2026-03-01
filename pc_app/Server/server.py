from fastapi import FastAPI, Header, HTTPException
from Server.auth import check_key, generate_key

from core.system_control import InfoManager, PowerManagement, LaunchProgram, RemoteVolume, ScreenBrightnessControl
from core .processes import ProcessManager
from core.file_manager import FileManager
from pydantic import BaseModel

class CreateFileBody(BaseModel):
    content: str

class EditBody(BaseModel):
    new_text: str

class ZipBody(BaseModel):
    zip_path: str

app = FastAPI()

SERVER_KEY = generate_key()

def auth_key(key: str):
    if key is None or not check_key(key):
        raise HTTPException(status_code=401, detail="Invalid API key")


@app.get("/info/system")
def system_info(x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {"status": "ok", "data": InfoManager.info_manager_json()}


# POWER
@app.get("/power/shutdown")
def shutdown_pc(x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {"status": "ok", "data": PowerManagement.shutdown()}

@app.get("/power/restart")
def restart_pc(x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {"status": "ok", "data": PowerManagement.restart()}

@app.get("/power/sleep")
def sleep_pc(x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {"status": "ok", "data": PowerManagement.sleep()}

@app.get("/power/hibernate")
def hibernate_pc(x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {"status": "ok", "data": PowerManagement.hibernate()}


# VOLUME
@app.get("/volume/mute")
def volume_mute(x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {"status": "ok", "data": RemoteVolume.mute()}

@app.get("/volume/unmute")
def volume_unmute(x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {"status": "ok", "data": RemoteVolume.unmute()}

@app.get("/volume/setVolume/{value}")
def volume_set(value: int, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {"status": "ok", "data": RemoteVolume.set_volume(value)}

@app.get("/volume/getVolume")
def volume_get(x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {"status": "ok", "data": RemoteVolume.get_volume()}


# BRIGHTNESS
@app.get("/brightness/getBrightness")
def brightness_get(x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {"status": "ok", "data": ScreenBrightnessControl.get_brightness()}

@app.get("/brightness/setBrightness/{value}")
def brightness_set(value: int, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {"status": "ok", "data": ScreenBrightnessControl.set_brightness(value)}


# PROGRAM
@app.get("/program/launch/{value}")
def launch_program(value: str, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {"status": "ok", "data": LaunchProgram.launch_program(value)}


# PROCESS
@app.get("/process/list")
def list_processes(x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {"status": "ok", "data": ProcessManager.list_processes()}

@app.get("/process/searchProcess/{value}")
def search_process(value: str, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {"status": "ok", "data": ProcessManager.search_process(value)}

@app.get("/process/kill/{value}")
def kill_process(value: int, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {"status": "ok", "data": ProcessManager.kill_process(value)}

@app.get("/process/start/{value}")
def start_process(value: str, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {"status": "ok", "data": ProcessManager.start_process(value)}

@app.get("/process/restartProcess/{value}")
def restart_process(value: int, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {"status": "ok", "data": ProcessManager.restart_process(value)}

@app.get("/process/info/{value}")
def info_process(value: int, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {"status": "ok", "data": ProcessManager.process_info(value)}


# FILE
@app.get("/file/searchfile/{value}")
def file_search(value: str, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {"status": "ok", "data": FileManager.searching_file(value)}

@app.get("/file/inspection/{path}")
def file_inspection(path: str, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {"status": "ok", "data": FileManager.inspection_of_folders(path)}

@app.post("/file/create/folder/{path}")
def create_folder(path: str, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {"status": "ok", "data": FileManager.create_folder(path)}

@app.post("/file/create/file/{path}")
def create_file(path: str, body: CreateFileBody, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {"status": "ok", "data": FileManager.create_file(path, body.content)}

@app.post("/file/create/zip/{source}")
def create_zip(source: str, body: ZipBody, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {"status": "ok", "data": FileManager.create_zip(source, body.zip_path)}

@app.delete("/file/delete/{path}")
def delete_file(path: str, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {"status": "ok", "data": FileManager.delete_item(path)}

@app.get("/file/read/{path}")
def read_file(path: str, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {"status": "ok", "data": FileManager.read_file(path)}

@app.put("/file/edit/{path}")
def edit_file(path: str, body: EditBody, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {"status": "ok", "data": FileManager.edit_file(path, body.new_text)}
