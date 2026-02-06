from fastapi import APIRouter
from auth.token_manager import create_token

route = APIRouter(prefix="/pc")

@route.get("/login")
def login(pc_id:str, key:str):
    if key != "1111":
        return {"error": "Invalid key"}

    token = create_token(pc_id)
    return {"token": token}

