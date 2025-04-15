import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
mongo_uri = os.getenv("MONGO_URI")

client = MongoClient(mongo_uri)

try:
    db = client["users_database"]
    db.test_conn.insert_one({"status":"ok"})
    print( list(db.test_conn.find())) 
    
    print("Banco conectado")
except Exception as e:
    print(f"error: {e}")