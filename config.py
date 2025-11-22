import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://MernAuth:admin1@cluster0.xpgba.mongodb.net/wafdb")
JWT_SECRET = os.getenv("JWT_SECRET", "f2d9c4a1b3e9f6d7a8c9e0f1d2b3a4c5e6f7d8a9b0c1d2e3f4a5b6c7d8e9f0a1")
RATE_LIMIT_DEFAULT = int(os.getenv("RATE_LIMIT_DEFAULT", "100"))
SOCKETIO_MESSAGE_QUEUE = os.getenv("SOCKETIO_MESSAGE_QUEUE", "")  # optional Redis URL

client = MongoClient(MONGO_URI)
DB = client.get_database("wafdb")  # ensure using 'wafdb' explicitly

# collections
USERS = DB["users"]
RULES = DB["waf_rules"]
LOGS = DB["logs"]
ALERTS = DB["alerts"]
ITEMS = DB["items"]
