import json
import httpx
from storage.sheme import get_pc_ip,get_pc_key,get_pc_port
from storage.connect import SessionLocal
import websockets
import base64

def pc_command_executor(command,arg1=None,arg2=None):
    cmd_map = {
        "info": [
            {"systeminfo": None}
        ],
        "power": [
            {"shutdown": None,
             "restart": None,
             "sleep": None,
             "hibernate": None}
        ],
        "volume": [
            {"mute": None,
             "unmute": None,
             "setvolume": "smth",
             "getvolume": None}
        ],
        "brightness": [
            {"getbrightness": None,
             "setbrightness": "smth"}
        ],
        "program": [
            {"launch": "smth",
             "listrunning":None,
             "close":"smth"}
        ],
        "process": [
            {"listprocesses": None,
             "searchprocess": "smth",
             "killprocess": "smth",
             "startprocess": "smth",
             "restartprocess": "smth",
             "infoprocess": "smth"}
        ],
        "file": [
            {"searchfile": "smth",
             "inspectfolder": "smth",
             "createfolder": "smth",
             "createfile":"smth",
             "createzip": ["smth","smth2"],
             "deleteitem": "smth",
             "readfile": "smth",
             "moveitem":["smth","smth"],
             "editfile": "smth"}
        ],
        "camera": [
            {
                "screenscreenshot":None,
                "cameracapture":None
            }
        ],
        "stream":[
            {
                "start":None,
                "end":None,
            }
        ]
    }

    for group, command_list in cmd_map.items():
        commands_dict = command_list[0]
        if command in commands_dict:
            command_type = commands_dict[command]
            if command_type is None:
                return f"/{group}/{command}"
            if command_type == "smth":
                if arg1 is None:
                    return None
                return f"/{group}/{command}/{arg1}"
            if isinstance(command_type, list):
                if arg1 is None or arg2 is None:
                    return None
                return f"/{group}/{command}/{arg1}/{arg2}"

    return None


async def execute_command(pc_id, command_str: str, content: str = None):
    parts = command_str.split(" ", 3)
    if len(parts) == 1:
        command = parts[0]
        arg1, arg2 = None, None
    elif len(parts) == 2:
        command = f"{parts[0]}{parts[1]}"
        arg1, arg2 = None, None
    else:
        command = f"{parts[0]}{parts[1]}"
        arg1, arg2 = parts[2], None
        if len(parts) > 3:
            arg2 = parts[3]

    url_path = pc_command_executor(command, arg1, arg2)
    print("command: ", command)
    print("Arg1: ",arg1)
    print("Arg2: ",arg2)
    print("URL: ",url_path)
    print("Conetnt: ", content)
    if url_path is None:
        return {"error": "Unknown command"}
    db = SessionLocal()
    pc_ip = get_pc_ip(db, pc_id)
    pc_port = get_pc_port(db, pc_id)
    x_api_key = get_pc_key(db, pc_id)
    db.close()
    url = f"http://{pc_ip}:{pc_port}{url_path}"
    timeout = httpx.Timeout(300.0, connect=10.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        if command == "editfile":
            r = await client.post(url, headers={"x-api-key": x_api_key}, json={"content": content})
        else:
            r = await client.get(url, headers={"x-api-key": x_api_key})

    return r.json()

async def WS_execute_command(pc_id, command_str: str, content: str = None):
    parts = command_str.split(" ", 3)
    if len(parts) == 1:
        command = parts[0]
        arg1, arg2 = None, None
    elif len(parts) == 2:
        command = f"{parts[0]}{parts[1]}"
        arg1, arg2 = None, None
    else:
        command = f"{parts[0]}{parts[1]}"
        arg1, arg2 = parts[2], None
        if len(parts) > 3:
            arg2 = parts[3]

    url_path = pc_command_executor(command, arg1, arg2)
    if url_path is None:
        yield {"error": "Unknown command"}
        return

    db = SessionLocal()
    pc_ip = get_pc_ip(db, pc_id)
    pc_port = get_pc_port(db, pc_id)
    x_api_key = get_pc_key(db, pc_id)
    db.close()

    pc_url = f"ws://{pc_ip}:{pc_port}{url_path}?x_api_key={x_api_key}"
    print("Connecting to PC via WS:", pc_url)

    try:
        async with websockets.connect(pc_url) as ws:
            while True:
                frame_str = await ws.recv()
                data = json.loads(frame_str)

                yield data
                print("data:", data)

    except Exception as e:
        print(f"WS connection error: {e}")
        yield {"error": f"WS connection error: {e}"}




