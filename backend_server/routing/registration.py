from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel

from storage.model import User, Clients
from storage.connect import SessionLocal
from auth.token_manager import create_token

router = APIRouter()

class PCData(BaseModel):
    pc_ip: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/client/register_pc")
def register_pc(data: PCData, request: Request, db: Session = Depends(get_db)):
    pc_ip = data.pc_ip
    user_ip = request.client.host

    print(f"Received registration from user_ip={user_ip}, pc_ip={pc_ip}")

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
        pc = Clients(pc_ip=pc_ip, owner=user)
        db.add(pc)
        db.commit()
        db.refresh(pc)

    token = create_token(user.user_id)
    user.jwt = token
    db.commit()

    return {
        "status": "ok",
        "user_id": user.user_id,
        "jwt": token,
        "pcs": [{"pc_id": c.pc_id, "pc_ip": c.pc_ip} for c in user.pcs]
    }