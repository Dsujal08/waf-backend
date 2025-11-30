import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://MernAuth:admin1@cluster0.xpgba.mongodb.net/wafdb")

client = MongoClient(MONGO_URI)
DB = client.get_database("wafdb")

# Collections
USERS = DB["users"]
LOGS = DB["LOGS"]
RULES = DB["waf_rules"]
ALERTS = DB["alerts"]
ITEMS = DB["items"]
