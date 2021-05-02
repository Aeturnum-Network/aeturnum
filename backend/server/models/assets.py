from typing import Optional, List
from pydantic import BaseModel, HttpUrl
from uuid import UUID
import datetime


class AssetCreate(BaseModel):
    name: str
    public_key: str
    private_key: str
    base_url: HttpUrl


class AssetUpdate(BaseModel):
    name: Optional[str]
    public_key: Optional[str]
    private_key: Optional[str]
    base_url: Optional[HttpUrl]


class Asset(AssetCreate):
    id: UUID
    user_id: str
