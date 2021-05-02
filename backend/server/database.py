from motor.motor_asyncio import AsyncIOMotorClient

from server.models.users import UserDB
from server.config import *
from server.models.users import UserCreate

class DataBase:
    client: AsyncIOMotorClient = None


db = DataBase()


async def get_database() -> AsyncIOMotorClient:
    return db.client[DB_NAME]


async def connect_to_mongo():
    print("Connecting to database...")
    db.client = AsyncIOMotorClient(MONGO_ENDPOINT)
    print("Connected!")


async def close_mongo_connection():
    print("Disconnecting from database...")
    db.client.close()
    print("Disconnected！")


async def init_superuser():
    from server.routes.users import fastapi_users
    
    print("Initializing superuser...")
    db = await get_database()

    suser = await db["users"].find_one({"email": SUPERUSER_EMAIL})
    if suser:
        print("Super User already exists")
    else:
        superuser = await fastapi_users.create_user(
            UserCreate(
                email=SUPERUSER_EMAIL,
                password=SUPERUSER_PASSWORD,
                is_superuser=True,
                first_name="Super",
                last_name="User",
            )
        )
        superuser = await fastapi_users.create_user(
            UserCreate(
                email="dev@aeturnum.ai",
                password="password",
                is_superuser=True,
                first_name="Dev",
                last_name="User",
            )
        )
        print("Super User created")

    print("Initialized!")