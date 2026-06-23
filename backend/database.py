import os
import certifi
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
if not MONGODB_URI:
    print("WARNING: MONGODB_URI environment variable is empty or not set. Defaulting to local MongoDB: mongodb://localhost:27017")
    MONGODB_URI = "mongodb://localhost:27017"
DB_NAME = "northstar_db"

client = None
db = None

def get_db():
    return db

async def connect_to_mongo():
    global client, db
    client = AsyncIOMotorClient(MONGODB_URI, tlsCAFile=certifi.where())
    db = client[DB_NAME]
    print("Connected to MongoDB!")

async def close_mongo_connection():
    global client
    if client:
        client.close()
        print("Disconnected from MongoDB!")
