import httpx
from storage.sheme import get_pc_ip
from storage.connect import SessionLocal


def pc_command_executor(pc_id, command,arg=None):
    cmd_map = {
        "info": [
            {"system": None}
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
             "setVolume": "smth",
             "getVolume": None}
        ],
        "brightness": [
            {"getBrightness": None,
             "setBrightness": "smth"}
        ],
        "program": [
            {"launch": None}
        ],
        "process": [
            {"list": None,
             "searchProcess": "smth",
             "kill": "smth",
             "start": "smth",
             "restartProcess": "smth",
             "info": "smth"}
        ],
        "file": [
            {"searchfile": "smth",
             "inspection": "smth",
             "create/folder": "smth",
             "create/file": "smth",
             "create/zip": "smth",
             "delete": "smth",
             "read": "smth",
             "edit": "smth"}
        ]
    }

    for group,command_list in cmd_map.items():
        commands_dict = command_list[0]
        if command in commands_dict:
            if commands_dict[command] is None:
                url = f"/{group}/{command}"
            elif commands_dict[command] == "smth":
                url = f"/{group}/{command}/{arg}"
            return url

    return None

def get_pc_ip(pc_id):
    db = SessionLocal()
    ip = get_pc_ip(db, pc_id)
    db.close()

    return ip

async def execute_command(pc_id: str, command: str):
    command , arg = command.split(" ",1)
    url_path = execute_command(pc_id,command,arg)
    if url_path is None:
        return {"error":"Unknown command"}

    pc_ip= get_pc_ip(pc_id)
    url = f"http://{pc_ip}:8000{url_path}"

    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(url)
            return r.json()
    except httpx.RequestError as e:
        return {"error": f"Failed to connect to PC {pc_id}: {e}"}



