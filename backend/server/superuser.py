import subprocess
from uuid import UUID, uuid4

from server.config import *
from server.database import get_database
from server.routes.users import fastapi_users
from server.models.users import UserCreate


async def init_superuser():
    print("Initializing superuser...")
    db = await get_database()

    scompany = await db["companies"].find_one({"name": SUPERUSER_COMPANY})
    if scompany:
        company_id = scompany["id"]
        print("Super Company already exists")
    else:
        scompany = {
            "id": str(uuid4()),
            "name": SUPERUSER_COMPANY,
            "employee_cap": 100,
            "domain": "legal",
        }
        company_id = scompany["id"]
        await db["companies"].insert_one(scompany)
        print("Super Company created")

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
                company_admin=True,
                can_upload=True,
                company_id=company_id,
            )
        )
        print("Super User created")

    group = await db["groups"].find_one({"name": TEST_GROUP, "company_id": company_id})
    if group:
        print("Test group already exists")
    else:
        group = {
            "id": str(uuid4()),
            "name": TEST_GROUP,
            "company_id": company_id,
            "host_key": "alpha",
            "size": 0,
            "documents": 0,
            "hit_count": 0,
        }

        await db["groups"].insert_one(group)
        print("Test group created")

    print("Initialized!")
