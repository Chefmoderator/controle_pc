from fastapi import WebSocket
from pydantic.v1.validators import anystr_strip_whitespace

from storage.connected_devices import register_pc , unregister_pc

async def handle_pc_connection(pc_id:str, websocket: WebSocket):
    await websocket.accept()

    register_pc(pc_id, websocket)

    try:
        while True:
            msg = await websocket.receive_text()
            print(f"[PC {pc_id}] => {msg}")

    except Exception:
        unregister_pc(pc_id)

