from jose import jwt
from datetime import datetime, timedelta

SECRET = "Locked"

def create_token(pc_id: str):
    payload = {
        "pc_id":pc_id,
        "exp":datetime.utcnow() + timedelta(hours=12)
    }

    return jwt.encode(payload, SECRET, algorithm="HS256")

def verify_token(token: str):
    try:
        data = jwt.decode(token, SECRET, algorithms=["HS256"])
        return data["pc_id"]
    except:
        return None
