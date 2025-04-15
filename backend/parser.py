import os
from dotenv import load_dotenv
from pymongo import MongoClient
import json
from dateutil import parser
from dataclasses import asdict, dataclass
from datetime import datetime

@dataclass
class UserPreferences:
    timezone: str

@dataclass
class User:
    username: str
    password: str
    roles: list
    preferences: UserPreferences
    active: bool
    created_ts: float

def parse_users(data):
    def parse_roles(roles:dict) -> list[str]:
        return [
            key.replace("is_user_","")
            for key, value in roles.items()
            if value
        ]
    roles = {
    "is_user_admin": data["is_user_admin"],
    "is_user_manager": data["is_user_manager"],
    "is_user_tester": data["is_user_tester"]
    }   
    
    return User(
        username=data["user"],
        password=data["password"],
        roles= parse_roles(roles),
        preferences=UserPreferences(data["user_timezone"]),
        active=data["is_user_active"],
        created_ts=datetime.fromisoformat(data["created_at"].replace("Z", "+00:00")).timestamp(),
    )
           

def main():
    load_dotenv()
    cliente = MongoClient(os.getenv('MONGO_URI'))
    db = cliente['users_database']
    users_collection = db['users']
    

    if len(list(users_collection.find())) == 0:    
        with open('udata.json', 'r', encoding='utf-8') as f:
            udata = json.load(f)["users"]
            
            users = [parse_users(item) for item in udata]
            users_dict = [asdict(user) for user in users]

            users_collection.insert_many(users_dict)
            
            print('Users successfully imported')
    else: 
        print('Database not empty')
        
            

if __name__ == "__main__":
    main()

