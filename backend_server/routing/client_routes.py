from fastapi import APIRouter, HTTPException, Depends, WebSocketDisconnect ,WebSocket ,Request
from storage.pc_command_executor import execute_command, WS_execute_command
from auth.token_manager import verify_token
import httpx
import json
from sqlalchemy.orm import Session
from pydantic import BaseModel
from storage.model import User, Clients
from storage.connect import SessionLocal
from auth.token_manager import create_token


router = APIRouter(prefix="/client")

class RemovePCData(BaseModel):
    pc_id: int

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class CommandData(BaseModel):
    pc_id: str
    command: str
    token: str
    content: str = None

class PCData(BaseModel):
    pc_ip: str
    pc_port: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register_pc")
async def register_pc(data: PCData, request: Request, db: Session = Depends(get_db)):
    pc_ip = data.pc_ip
    pc_port = data.pc_port
    user_ip = request.client.host

    async with httpx.AsyncClient() as client:
        r = await client.get(f"http://{pc_ip}:8000/get_api_key")
        pc_key = r.json().get("pc_key")

    print(f"Received registration from user_ip={user_ip}, pc_ip={pc_ip}, pc_port={pc_port}")

    user = db.query(User).filter(User.user_ip == user_ip).first()
    if not user:
        user = User(user_ip=user_ip)
        db.add(user)
        db.commit()
        db.refresh(user)

    pc = db.query(Clients).filter(Clients.pc_ip == pc_ip).first()

    if pc and pc.user_id != user.user_id:
        raise HTTPException(400, "PC already linked to another user")

    if not pc:
        pc = Clients(pc_ip=pc_ip, owner=user, pc_key=pc_key, pc_port=pc_port)
        db.add(pc)
        db.commit()
        db.refresh(pc)

    token = create_token(user.user_id, pc.pc_id)
    user.jwt = token
    db.commit()

    return {
        "status": "ok",
        "user_id": user.user_id,
        "jwt": token,
        "pcs": [{"pc_id": c.pc_id, "pc_ip": c.pc_ip, "pc_port": c.pc_port} for c in user.pcs]
    }


@router.post("/send_command")
async def send_command(data: CommandData):
    pc_id = data.pc_id
    command = data.command
    token = data.token

    content = getattr(data, "content", None)
    if not content or content == "None":
        content = None

    command = command.lower()
    token_data = verify_token(token)

    if token_data is None or token_data["pc_id"] != int(pc_id):
        raise HTTPException(403, "Unauthorized")

    result = await execute_command(pc_id,command,content)

    if "error" in result:
        raise HTTPException(503, result["error"])

    return {"status": "ok", "data": result.get("data")}


@router.websocket("/ws_send_command")
async def ws_send_command(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            data = await ws.receive_text()
            payload = json.loads(data)
            verify_token(payload["token"])

            async for frame in WS_execute_command(
                payload["pc_id"],
                payload["command"],
                payload.get("content")
            ):

                await ws.send_text(json.dumps(frame))
    except WebSocketDisconnect:
        pass


@router.post("/remove_pc")
def remove_pc(data: RemovePCData, db: Session = Depends(get_db)):
    pc = db.query(Clients).filter(Clients.pc_id == data.pc_id).first()
    if not pc:
        raise HTTPException(status_code=404, detail="PC not found")

    db.delete(pc)
    db.commit()

    return {
        "status": "ok",
        "message": f"PC with id {data.pc_id} has been removed"
    }