from motor.motor_asyncio import AsyncIOMotorClient
from uuid import UUID, uuid4

from server.models.companies import *
from server.models.users import *


async def add_company(db: AsyncIOMotorClient, company_in: CompanyIn):
    company = company_in.dict()
    company["id"] = str(uuid4())
    await db["companies"].insert_one(company)
    return CompanyOut(**company)


async def find_my_company(db: AsyncIOMotorClient, user: User):
    company = await db["companies"].find_one({"id": user.company_id})
    if company:
        return CompanyOut(**company)


async def find_all_users(db: AsyncIOMotorClient, user: User):
    users = db["users"].find({"company_id": user.company_id})
    return [User(**user) async for user in users]


async def find_all_companies(db: AsyncIOMotorClient, user: User):
    companies = db["companies"].find()
    return [CompanyOut(**company) async for company in companies]


async def find_document_tree(db: AsyncIOMotorClient, user: User):
    documents = db["documents"].find({"company_id": user.company_id})
    groups = db["groups"].find({"company_id": user.company_id})

    tree = {
        group["id"]: {"name": group["name"], "documents": []} async for group in groups
    }

    async for document in documents:
        tree[document["group_id"]]["documents"].append(
            {
                "id": document["id"],
                "name": document["name"],
                "upload_status": document["upload_status"],
            }
        )

    return tree
