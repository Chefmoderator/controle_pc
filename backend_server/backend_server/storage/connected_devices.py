import asyncio
from datetime import datetime
import uuid


_connected = {}
_pending_commands = {}
_tasks_ = {}
user_connections = {}
pc_data_store = {}


def register_pc(pc_id, websocket):
    _connected[pc_id] = websocket
    _pending_commands[pc_id] = {}

def unregister_pc(pc_id):
    _connected.pop(pc_id, None)
    futures = _pending_commands.pop(pc_id, {})
    for fut in futures.values():
        if not fut.done():
            fut.set_exception(RuntimeError("PC disconnected"))

def get_pc_socket(pc_id):
    return _connected.get(pc_id)

def create_pending(pc_id, cmd_id):
    fut = asyncio.get_event_loop().create_future()
    if pc_id not in _pending_commands:
        _pending_commands[pc_id] = {}
    _pending_commands[pc_id][cmd_id] = fut
    return fut

def set_response(pc_id, cmd_id, result):
    fut = _pending_commands.get(pc_id, {}).pop(cmd_id, None)
    if fut and not fut.done():
        fut.set_result(result)

def add_task(pc_id, command, token):
    task_id = str(uuid.uuid4())
    _tasks_[task_id] = {
        "pc_id": pc_id,
        "command": command,
        "token": token,
        "status": "pending",
        "result": None,
        "created_at": datetime.utcnow().isoformat()
    }
    return task_id

def add_pc_data(pc_id: int, data: dict):
    if pc_id not in pc_data_store:
        pc_data_store[pc_id] = []
    pc_data_store[pc_id].append(data)

def get_pc_data(pc_id: int):
    return pc_data_store.pop(pc_id, [])

def register_user(pc_id: str, websocket):
    user_connections[pc_id] = websocket

def unregister_user(pc_id: str):
    user_connections.pop(pc_id, None)

def get_user_ws(pc_id: str):
    return user_connections.get(pc_id)