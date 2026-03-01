import os
import uuid

AUTH_FILE= "12142143252"

def generate_key():
    if not os.path.exists(AUTH_FILE):
        token = uuid.uuid4().hex
        with open(AUTH_FILE, "w") as f:
            f.write(token)
    else:
        with open(AUTH_FILE) as f:
            token = f.read().strip()

    return token

def check_key(client_key: str) -> bool:
    if not os.path.exists(AUTH_FILE):
        return False

    with open(AUTH_FILE) as f:
        real = f.read().strip()

    return client_key == real

