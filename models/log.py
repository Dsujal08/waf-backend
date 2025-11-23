from config import LOGS
from datetime import datetime

def log_request(data: dict):
    """Store log entry in MongoDB"""
    log_entry = {
        "timestamp": datetime.utcnow(),
        **data
    }
    LOGS.insert_one(log_entry)

def get_logs():
    """Retrieve all logs, newest first"""
    return list(LOGS.find().sort("timestamp", -1))
