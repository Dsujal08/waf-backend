# services/alert_service.py
from config import ALERTS
from datetime import datetime

def create_alert(doc):
    """Insert a new alert into MongoDB"""
    doc["timestamp"] = datetime.utcnow()
    doc["status"] = "unread"
    ALERTS.insert_one(doc)

def list_alerts(limit=50):
    """Return the latest alerts"""
    cursor = ALERTS.find({}).sort("timestamp", -1).limit(limit)
    out = []
    for d in cursor:
        d["_id"] = str(d["_id"])
        d["timestamp"] = d["timestamp"].isoformat() if d.get("timestamp") else None
        out.append(d)
    return out
