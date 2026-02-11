from fastapi import APIRouter, HTTPException
from storage.pc_command_executor import execute_command
from auth.token_manager import verify_token
import httpx

router = APIRouter(prefix="/client")

@router.post("/send_command")
async def send_command(pc_id: str, command: str, token: str):
    token_data = verify_token(token)
    if token_data is None or token_data["pc_id"] != pc_id:
        raise HTTPException(403, "Unauthorized")

    url = await execute_command(pc_id, command)
    if url is None:
        raise HTTPException(404, "Unknown command")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            data = response.json()
    except Exception as e:
        raise HTTPException(503, f"PC offline: {e}")

    return {"status": "ok", "data": data["data"]}
