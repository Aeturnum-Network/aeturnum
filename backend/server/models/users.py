from fastapi_users import models
from typing import Optional


class User(models.BaseUser):
    first_name: str
    last_name: str
    heir_id: str = ''


class UserCreate(models.BaseUserCreate):
    first_name: str
    last_name: str


class UserUpdate(User, models.BaseUserUpdate):
    first_name: Optional[str]
    last_name: Optional[str]
    heir_id: Optional[str]

class UserDB(User, models.BaseUserDB):
    pass
