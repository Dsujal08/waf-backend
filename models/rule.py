from config import RULES
from datetime import datetime
from bson import ObjectId

def list_rules():
    docs = list(RULES.find({}).sort("createdAt", -1))
    for d in docs:
        d["_id"] = str(d["_id"])
    return docs

def create_rule(doc):
    doc["createdAt"] = datetime.utcnow()
    doc["isActive"] = doc.get("isActive", True)
    res = RULES.insert_one(doc)
    return str(res.inserted_id)

def update_rule(rule_id, patch):
    RULES.update_one({"_id": ObjectId(rule_id)}, {"$set": patch})

def delete_rule(rule_id):
    RULES.delete_one({"_id": ObjectId(rule_id)})
