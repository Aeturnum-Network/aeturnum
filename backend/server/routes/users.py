from fastapi import Depends
from fastapi_users import FastAPIUsers
from fastapi_users.db import MongoDBUserDatabase
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import APIRouter, Body, Depends, Path, Query
from starlette.status import *
from starlette.exceptions import HTTPException
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from uuid import UUID, uuid4

from server.models.users import *
from server.config import *
from server.database import get_database

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

router = APIRouter()

@router.post("/{id}/deactivate", response_model=User, status_code=HTTP_200_OK)
async def deactivate_user(
    id,
    db: AsyncIOMotorClient = Depends(get_database),
    user: User = Depends(fastapi_users.get_current_user),
):
    if user.heir_id != '':
        assets = db["assets"].find({"user_id": str(user.id)})
        await db["assets"].update_many({'user_id': str(user.id)}, {'$set': {'user_id': str(user.heir_id)}})
    
    await db["users"].update_one({'email': user.email}, {'$set': {'is_active': False}})
    user = await db["users"].find_one({'email': user.email})
    return User(**user)
