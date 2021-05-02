from fastapi import APIRouter, Body, Depends, Path, Query
from starlette.status import *
from starlette.exceptions import HTTPException
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from uuid import UUID, uuid4

from server.config import *
from server.database import get_database
from server.models.assets import *
from server.models.users import *
from server.routes.users import fastapi_users

router = APIRouter()

@router.post("", response_model=Asset, status_code=HTTP_201_CREATED)
async def create_asset(
    asset: AssetCreate,
    db: AsyncIOMotorClient = Depends(get_database),
    user: User = Depends(fastapi_users.get_current_user),
):
    asset = asset.dict()
    asset["id"] = str(uuid4())
    asset["user_id"] = str(user.id)
    await db["assets"].insert_one(asset)

    return Asset(**asset)


@router.get("", response_model=List[Asset], status_code=HTTP_200_OK)
async def get_all_assets(
    db: AsyncIOMotorClient = Depends(get_database),
    user: User = Depends(fastapi_users.get_current_user),
):
    assets = db["assets"].find({"user_id": str(user.id)})
    return [Asset(**asset) async for asset in assets]


@router.get("/{id}", response_model=Asset, status_code=HTTP_200_OK)
async def get_asset(
    id,
    db: AsyncIOMotorClient = Depends(get_database),
    user: User = Depends(fastapi_users.get_current_user),
):
    asset = await db["assets"].find_one({"id": id, "user_id": str(user.id)})
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return Asset(**asset)


@router.delete("/{id}", status_code=HTTP_200_OK)
async def delete_asset(
    id,
    db: AsyncIOMotorClient = Depends(get_database),
    user: User = Depends(fastapi_users.get_current_user),
):

    asset = await db["assets"].find_one({"id": id, "user_id": str(user.id)})
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    await db["assets"].delete_one({"id": id, "user_id": str(user.id)})

    return Asset(**asset)
