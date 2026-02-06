from fastapi import APIRouter, HTTPException
from storage.connected_devices import get_pc_socket
from auth.token_manager import verify_token

router = APIRouter(prefix="/client")

@router.post("/send_command")
async def send_command(pc_id:str, command:str, token:str):
    owner = verify_token(token)
    if owner != pc_id:
        raise HTTPException(401, "Invalid token")

    pc_socket = get_pc_socket(pc_id)

    if pc_socket is None:
        raise HTTPException(404, "PC offline")

    await pc_socket.send_text(command)
    return {"status": "sent"}