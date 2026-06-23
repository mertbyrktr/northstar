import os
import certifi
from motor.motor_asyncio import AsyncIOMotorClient
import redis.asyncio as redis
from dotenv import load_dotenv
from rabbitmq import connect_rabbitmq, close_rabbitmq

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
if not MONGODB_URI:
    print("WARNING: MONGODB_URI environment variable is empty or not set. Defaulting to local MongoDB: mongodb://localhost:27017")
    MONGODB_URI = "mongodb://localhost:27017"
DB_NAME = "northstar_db"

REDIS_URL = os.getenv("REDIS_URL")
if not REDIS_URL:
    print("WARNING: REDIS_URL environment variable is empty or not set. Defaulting to local Redis: redis://localhost:6379/0")
    REDIS_URL = "redis://localhost:6379/0"

client = None
db = None
redis_client = None

def get_db():
    return db

def get_redis():
    return redis_client

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

async def connect_to_redis():
    global redis_client
    # decode_responses=True decodes bytes returned from redis to unicode strings
    redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    try:
        await redis_client.ping()
        print("Connected to Redis!")
    except Exception as e:
        print(f"Error connecting to Redis: {e}")

async def close_redis_connection():
    global redis_client
    if redis_client:
        await redis_client.aclose()
        print("Disconnected from Redis!")

async def connect_to_rabbitmq():
    await connect_rabbitmq()

async def close_rabbitmq_connection():
    await close_rabbitmq()
