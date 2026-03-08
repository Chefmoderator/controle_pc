import httpx
from storage.sheme import get_pc_ip,get_pc_key
from storage.connect import SessionLocal


def pc_command_executor(command,arg=None):
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

            return url;

    return None


async def execute_command(pc_id, command_str: str):
    parts = command_str.split(" ", 2)
    print("Part 1: ", parts[0])
    print("Parts 2: ", parts[1])
    print("Parts 3: ", parts[2])
    if len(parts) == 1:
        command = parts[0]
        arg = None
    elif len(parts) == 2:
        command = f"{parts[0]}{parts[1]}"
        arg = None
    else:
        command = f"{parts[0]}{parts[1]}"
        arg = parts[2]
    print("Command: ",command)
    url_path = pc_command_executor(command, arg)
    print("Url path: ",url_path)
    if url_path is None:
        return {"error": "Unknown command"}

    db = SessionLocal()
    pc_ip = get_pc_ip(db, pc_id)
    x_api_key = get_pc_key(db, pc_id)
    db.close()

    url = f"http://{pc_ip}:8000{url_path}"
    try:
        timeout = httpx.Timeout(300.0, connect=10.0)

        async with httpx.AsyncClient(timeout=timeout) as client:
            r = await client.get(url, headers={"x-api-key": x_api_key})
            print("Read:", r)
            return r.json()
    except httpx.RequestError as e:
        return {"error": f"Failed to connect to PC {pc_id}: {e}"}



