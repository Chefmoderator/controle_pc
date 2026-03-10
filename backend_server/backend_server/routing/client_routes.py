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
    content: str = None

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