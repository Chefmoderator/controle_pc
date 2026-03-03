from fastapi import APIRouter, HTTPException, Depends
from storage.pc_command_executor import execute_command
from auth.token_manager import verify_token
import httpx
from sqlalchemy.orm import Session
from pydantic import BaseModel
from storage.model import User, Clients
from storage.connect import SessionLocal

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

@router.post("/send_command")
async def send_command(data: CommandData):
    pc_id = data.pc_id
    command = data.command
    token = data.token
    command = command.lower()

    token_data = verify_token(token)

    if token_data is None or token_data["pc_id"] != int(pc_id):
        raise HTTPException(403, "Unauthorized")
    url = await execute_command(pc_id,command)
    print("url: ", url)
    if url is None:
        raise HTTPException(404, "Unknown command")
    print(3)
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            data = response.json()
    except Exception as e:
        raise HTTPException(503, f"PC offline: {e}")

    return {"status": "ok", "data": data["data"]}


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