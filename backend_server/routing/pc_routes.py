from fastapi import APIRouter, HTTPException
from auth.token_manager import verify_token
from typing import Any
from storage.connected_devices import add_pc_data, get_user_ws
import asyncio

router = APIRouter(prefix="/pc")

@router.post("/send_data")
async def pc_send_data(pc_id: int, data: dict, token: str):
    token_data = verify_token(token)
    if token_data is None or token_data["pc_id"] != pc_id:
        raise HTTPException(403, "Unauthorized PC")

    add_pc_data(pc_id, data)

    user_ws = get_user_ws(pc_id)

    if user_ws:
        try:
            await user_ws.send_json({"pc_id":pc_id, "data":data})
        except Exception:
            pass

    return {"status":"ok"}
