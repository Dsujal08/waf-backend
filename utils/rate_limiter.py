import time
from config import RATE_LIMIT_DEFAULT

_store = {}

def hit(ip):
    now = time.time()
    window = 60
    state = _store.get(ip)
    if not state or now - state["ts"] > window:
        _store[ip] = {"ts": now, "count": 1}
        return False
    else:
        state["count"] += 1
        _store[ip] = state
        return state["count"] > RATE_LIMIT_DEFAULT
