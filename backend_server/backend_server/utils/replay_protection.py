import time

_seen_nonces = set()

def check_replay(msg: str) -> bool:
    try:
        parts = msg.split("|")
        nonce = parts[-1]
        if nonce in _seen_nonces:
            return False
        _seen_nonces.add(nonce)
        # Очистка старых nonces
        if len(_seen_nonces) > 10000:
            _seen_nonces.pop()
        return True
    except:
        return False
