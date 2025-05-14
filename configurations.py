from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

url = "mongodb://localhost:27017/"

client = MongoClient(url, server_api=ServerApi('1'))
db = client.todo_db

collection = db["todo_data"]
try:
    client.admin.command('ping')
    print("✅ Connected to local MongoDB")
except Exception as e:
    print("❌ Connection failed:", e)
