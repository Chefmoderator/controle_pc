from fastapi import FastAPI, Header, HTTPException
from auth import check_key, generate_key

from pc_app.core import InfoManager,PowerManagement, LaunchProgram,RemoteVolume,ScreenBrightnessControl
from pc_app.core import ProcessManager
from pc_app.core.file_manager import FileManager

app = FastAPI()

SERVER_KEY = generate_key()

def auth_key(key: str):
    if key is None or not check_key(key):
        raise HTTPException(status_code=401, detail="Invalid API key")

@app.get("/info/system")
def system_info(x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return InfoManager.info_manager_json()

#power
@app.get("/power/shutdown")
def shutdown_pc(x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    PowerManagement.shutdown()
    return {"status": "ok"}

@app.get("/power/restart")
def restart_pc(x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    PowerManagement.restart()
    return {"status": "ok"}

@app.get("/power/sleep")
def sleep_pc(x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    PowerManagement.sleep()
    return {"status": "ok"}

@app.get("/power/hibernate")
def hibernate_pc(x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    PowerManagement.hibernate()
    return {"status": "ok"}

#Volume
@app.get("/volume/mute")
def volume_mute(x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    RemoteVolume.mute()
    return {"status": "ok"}

@app.get("/volume/unmute")
def volume_unmute(x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    RemoteVolume.unmute()
    return {"status": "ok"}

@app.get("/volume/set/{value}")
def volume_set(value: int, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    RemoteVolume.set_volume(value)
    return {"status": "ok"}

@app.get("/volume/get")
def volume_get(x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {"volume": RemoteVolume.get_volume()}

#brightness
@app.get("/brightness/get")
def mute(x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {"brightness": ScreenBrightnessControl.get_brightness()}

@app.get("/brightness/set/{value}")
def mute(value:int ,x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    ScreenBrightnessControl.set_brightness(value)
    return {"status": "ok"}

#program
@app.get("/program/launch/{value}")
def launch_program(value: str, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    LaunchProgram.launch_program(value)
    return {"status":"ok"}

#process
@app.get("/process/list")
def list(x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return ProcessManager.list_processes()

@app.get("/process/search/{value}")
def search(value: str, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return ProcessManager.search_process(value)

@app.get("/process/kill/{value}")
def kill(value:int, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    ProcessManager.kill_process(value)
    return {"status":"ok"}

@app.get("/process/start/{value}")
def start(value:str, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    ProcessManager.start_process(value)
    return {"status":"ok"}

@app.get("/process/restart/{value}")
def restartPR(value:int, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    ProcessManager.restart_process(value)
    return {"status":"ok"}

@app.get("/process/info/{value}")
def infoPr(value:int, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return ProcessManager.process_info(value)

#File
@app.get("/file/search/{value}")
def searchF(value: str, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return FileManager.searching_file(value)


@app.get("/file/inspection/{path}")
def inspection(path: str, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return FileManager.inspection_of_folders(path)


@app.post("/file/create/folder/{path}")
def createfo(path: str, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return FileManager.create_folder(path)


@app.post("/file/create/file/{path}")
def createfl(path: str, body: CreateFileBody, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return FileManager.create_file(path, body.content)


@app.post("/file/create/zip/{source}")
def createz(source: str, body: ZipBody, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return FileManager.create_zip(source, body.zip_path)


@app.delete("/file/delete/{path}")
def delete(path: str, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return FileManager.delete_item(path)


@app.get("/file/read/{path}")
def read(path: str, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return FileManager.read_file(path)


@app.put("/file/edit/{path}")
def edit(path: str, body: EditBody, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return FileManager.edit_file(path, body.new_text)





