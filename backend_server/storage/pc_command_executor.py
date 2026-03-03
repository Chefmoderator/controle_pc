import httpx
from storage.sheme import get_pc_ip,get_pc_key
from storage.connect import SessionLocal


def pc_command_executor(command,arg=None):
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


async def execute_command(pc_id, command_str: str):
    parts = command_str.split(" ", 1)
    command = parts[0]
    arg = parts[1] if len(parts) > 1 else None
    url_path = pc_command_executor(command, arg)

    if url_path is None:
        return {"error": "Unknown command"}

    db = SessionLocal()
    pc_ip = get_pc_ip(db, pc_id)
    x_api_key = get_pc_key(db, pc_id)
    db.close()

    url = f"http://{pc_ip}:8000{url_path}"

    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(url, headers={"x-api-key": x_api_key})
            print("Read:", r)
            return r.json()
    except httpx.RequestError as e:
        return {"error": f"Failed to connect to PC {pc_id}: {e}"}



