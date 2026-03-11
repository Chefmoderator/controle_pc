from fastapi import FastAPI, Header, HTTPException
from starlette.websockets import WebSocket,WebSocketDisconnect
import json
from Server.auth import check_key, generate_key
from fastapi import Body
from pydantic import BaseModel


from core.system_control import InfoManager, PowerManagement, LaunchProgram, RemoteVolume, ScreenBrightnessControl
from core.processes import ProcessManager
from core.file_manager import FileManager
from core.camera_manager import CameraManager
from core.stream import Stream


class CreateFileBody(BaseModel):
    content: str

class EditBody(BaseModel):
    content: str

class ZipBody(BaseModel):
    zip_path: str

app = FastAPI()

SERVER_KEY = generate_key()


def auth_key(key: str):
    if key is None or not check_key(key):
        raise HTTPException(status_code=401, detail="Invalid API key")

@app.get("/get_api_key")
def get_api_key():
    return {"pc_key": SERVER_KEY}


@app.get("/info/systeminfo")
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

@app.get("/volume/setvolume/{value}")
def volume_set(value: int, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {"status": "ok", "data": RemoteVolume.set_volume(value)}

@app.get("/volume/getvolume")
def volume_get(x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {"status": "ok", "data": RemoteVolume.get_volume()}


# BRIGHTNESS
@app.get("/brightness/getbrightness")
def brightness_get(x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {"status": "ok", "data": ScreenBrightnessControl.get_brightness()}

@app.get("/brightness/setbrightness/{value}")
def brightness_set(value: int, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {"status": "ok", "data": ScreenBrightnessControl.set_brightness(value)}


# PROGRAM
@app.get("/program/launch/{value}")
def launch_program(value: str, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {
        "status": "ok",
        "data": LaunchProgram.launch_program(value)
    }

@app.get("/program/listrunning")
def list_running_program(x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {
        "status": "ok",
        "data": LaunchProgram.list_running_programs()
    }

@app.get("/program/close")
def close_program(pid:int, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {
        "status": "ok",
        "data": LaunchProgram.close_program(pid)
    }

# PROCESS
@app.get("/process/listprocesses")
def list_processes(x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {"status": "ok", "data": ProcessManager.list_processes()}

@app.get("/process/searchprocess/{value}")
def search_process(value: str, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {"status": "ok", "data": ProcessManager.search_process(value)}

@app.get("/process/killprocess/{value}")
def kill_process(value: int, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {"status": "ok", "data": ProcessManager.kill_process(value)}

@app.get("/process/startprocess/{value}")
def start_process(value: str, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {"status": "ok", "data": ProcessManager.start_process(value)}

@app.get("/process/restartprocess/{value}")
def restart_process(value: int, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {"status": "ok", "data": ProcessManager.restart_process(value)}

@app.get("/process/infoprocess/{value}")
def info_process(value: int, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {"status": "ok", "data": ProcessManager.process_info(value)}


# FILE
@app.get("/file/searchfile/{value}")
def file_search(value: str, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {"status": "ok", "data": FileManager.searching_file(value)}

@app.get("/file/inspectfolder/{path:path}")
def file_inspection(path: str, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {"status": "ok", "data": FileManager.inspection_of_folders(path)}

@app.get("/file/createfolder/{path}")
def create_folder(path: str, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {"status": "ok", "data": FileManager.create_folder(path)}

@app.get("/file/createfile/{full_path}")
def create_file(full_path: str, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    result = FileManager.create_file(full_path)
    return {"status": "ok", "data": result}

@app.get("/file/createzip/{source}")
def create_zip(source: str, body: ZipBody, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {"status": "ok", "data": FileManager.create_zip(source, body.zip_path)}

@app.get("/file/deleteitem/{path}")
def delete_file(path: str, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {"status": "ok", "data": FileManager.delete_item(path)}

@app.get("/file/readfile/{path}")
def read_file(path: str, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {"status": "ok", "data": FileManager.read_file(path)}

@app.get("/file/moveitem/{src}/{dst}")
def move_item(src: str,dst: str, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {"status":"ok", "data": FileManager.move_item(src, dst)}

@app.post("/file/editfile/{path}")
async def edit_file(path: str, content: EditBody, x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    print("Path: ",path)
    return {"status": "ok", "data": FileManager.edit_file(path, content.content)}

#camera
@app.get("/camera/screenscreenshot")
def get_screen(x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {"status":"ok", "data":CameraManager.get_screen()}

@app.get("/camera/cameracapture")
def get_camera(x_api_key: str = Header(default=None)):
    auth_key(x_api_key)
    return {"status":"ok", "data":CameraManager.get_camera()}

#stream
@app.websocket("/stream/start")
async def stream(ws: WebSocket):
    await ws.accept()
    x_api_key = ws.query_params.get("x_api_key")

    try:
        auth_key(x_api_key)
    except HTTPException:
        print("Auth failed")
        await ws.close(code=4401)
        return

    try:
        while True:
            frame_b64 = Stream.get_screen()
            await ws.send_text(json.dumps({"status": "ok", "data": frame_b64}))
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print("Stream closed:", e)
