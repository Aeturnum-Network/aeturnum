from fastapi import Depends
from fastapi_users import FastAPIUsers
from fastapi_users.db import MongoDBUserDatabase
from motor.motor_asyncio import AsyncIOMotorClient

from server.models.users import *
from server.config import *

client = AsyncIOMotorClient(MONGO_ENDPOINT, uuidRepresentation="standard")
db = client[DB_NAME]
collection = db["users"]
user_db = MongoDBUserDatabase(UserDB, collection)

fastapi_users = FastAPIUsers(
    user_db,
    AUTH_BACKENDS,
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)
