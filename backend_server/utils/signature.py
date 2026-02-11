import hmac, hashlib

SIGN_SECRET = b"supersecret"

def sign_command(command: str) -> str:
    signature = hmac.new(SIGN_SECRET, command.encode(), hashlib.sha256).hexdigest()
    return f"{command}|{signature}"

def verify_signature(msg: str) -> bool:
    try:
        command, signature = msg.rsplit("|", 1)
        expected = hmac.new(SIGN_SECRET, command.encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature)
    except:
        return False
