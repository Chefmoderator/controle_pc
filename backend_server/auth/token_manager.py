from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta

SECRET = "Locked"

def create_token(user_id: str, pc_id: str, role: str):
    payload = {
        "user_id": user_id,
        "pc_id": pc_id,
        "role": role,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=12)
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")

def verify_token(token: str):
    try:
        data = jwt.decode(token, SECRET, algorithms=["HS256"])
        return {
            "user_id": data.get("user_id"),
            "pc_id": data.get("pc_id"),
            "role": data.get("role")
        }
    except ExpiredSignatureError:
        print("Token expired")
        return None
    except JWTError:
        print("Invalid token")
        return None

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        print("Токен истёк")
        return None
    except jwt.InvalidTokenError:
        print("Неверный токен")
        return None