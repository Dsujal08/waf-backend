from config import LOGS
from datetime import datetime

def log_request(entry):
    entry["timestamp"] = datetime.utcnow()
    LOGS.insert_one(entry)

def get_logs(query=None, skip=0, limit=50):
    query = query or {}
    cursor = LOGS.find(query).sort("timestamp", -1).skip(skip).limit(limit)
    out = []
    for d in cursor:
        d["_id"] = str(d["_id"])
        d["timestamp"] = d.get("timestamp").isoformat() if d.get("timestamp") else None
        out.append(d)
    return out
