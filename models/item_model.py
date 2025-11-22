from config import items_collection
from bson.objectid import ObjectId

def get_all_items():
    data = list(items_collection.find())
    for item in data:
        item["_id"] = str(item["_id"])
    return data

def add_item(record):
    result = items_collection.insert_one(record)
    return str(result.inserted_id)

def get_item_by_id(id):
    return items_collection.find_one({"_id": ObjectId(id)})

def delete_item(id):
    return items_collection.delete_one({"_id": ObjectId(id)})
