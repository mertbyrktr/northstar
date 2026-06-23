import os
import jwt
import json
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from database import get_db, get_redis
from bson import ObjectId

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    # Try cache first
    redis_client = get_redis()
    cache_key = f"user:profile:{user_id}"
    if redis_client:
        try:
            cached_user = await redis_client.get(cache_key)
            if cached_user:
                return json.loads(cached_user)
        except Exception as e:
            print(f"Redis get error: {e}")

    db = get_db()
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if user is None:
        raise credentials_exception
    
    # Return user data with string ID
    user["id"] = str(user.pop("_id"))

    # Save to cache
    if redis_client:
        try:
            await redis_client.setex(cache_key, 300, json.dumps(user))
        except Exception as e:
            print(f"Redis set error: {e}")

    return user
