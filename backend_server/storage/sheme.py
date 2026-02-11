from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from storage.connect import SessionLocal
from storage.model import Clients

router = APIRouter(prefix="/pc_db")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/add")
def add_pc(pc_id: int, pc_ip: str, db: Session = Depends(get_db)):
    existing = db.query(Clients).filter(Clients.pc_id == pc_id).first()
    if existing:
        raise HTTPException(400, "PC already exists")

    new_pc = Clients(pc_id=pc_id, pc_ip=pc_ip)
    db.add(new_pc)
    db.commit()
    db.refresh(new_pc)
    return {"status": "ok", "data": {"pc_id": new_pc.pc_id, "pc_ip": new_pc.pc_ip}}


@router.get("/list")
def list_pcs(db: Session = Depends(get_db)):
    pcs = db.query(Clients).all()
    return {"status": "ok", "data": [{"pc_id": pc.pc_id, "pc_ip": pc.pc_ip} for pc in pcs]}

def get_pc_ip(db: Session, pc_id: int):
    pc = db.query(Clients).filter(Clients.pc_id == pc_id).first()
    if pc:
        return pc.pc_ip
    return None