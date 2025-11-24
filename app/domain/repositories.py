from datetime import datetime
from typing import Optional, Union

from bson import ObjectId  # comes with pymongo

from app.infrastructure.db import (
    companies_collection,
    employees_collection,
    jobs_collection,
)


ObjectIdLike = Union[ObjectId, str]


def _to_object_id(value: ObjectIdLike) -> ObjectId:
    if isinstance(value, ObjectId):
        return value
    return ObjectId(value)


# ---------- COMPANIES (OWNERS) ----------

async def get_company_by_owner(owner_telegram_id: int) -> Optional[dict]:
    return await companies_collection.find_one({"owner_telegram_id": owner_telegram_id})


async def get_company_by_code(code: str) -> Optional[dict]:
    return await companies_collection.find_one({"code": code})


async def get_company_by_id(company_id: ObjectIdLike) -> Optional[dict]:
    oid = _to_object_id(company_id)
    return await companies_collection.find_one({"_id": oid})


async def create_company(
    owner_telegram_id: int,
    owner_chat_id: int,
    name: str | None = None,
) -> dict:
    # Simple deterministic company code based on owner id
    code = f"CO-{owner_telegram_id % 100000:05d}"

    doc = {
        "owner_telegram_id": owner_telegram_id,
        "owner_chat_id": owner_chat_id,
        "name": name or "My Construction Company",
        "code": code,
        "created_at": datetime.utcnow(),
    }

    result = await companies_collection.insert_one(doc)
    doc["_id"] = result.inserted_id
    return doc


# ---------- EMPLOYEES ----------

async def upsert_employee(
    company_id: ObjectIdLike,
    telegram_id: int,
    chat_id: int,
    full_name: str | None = None,
) -> dict:
    company_oid = _to_object_id(company_id)
    now = datetime.utcnow()

    # Update if exists, otherwise create
    await employees_collection.update_one(
        {"telegram_id": telegram_id},
        {
            "$set": {
                "company_id": company_oid,
                "telegram_id": telegram_id,
                "chat_id": chat_id,
                "full_name": full_name,
                "updated_at": now,
            },
            "$setOnInsert": {"created_at": now},
        },
        upsert=True,
    )

    employee = await employees_collection.find_one({"telegram_id": telegram_id})
    return employee


async def get_employee_by_telegram(telegram_id: int) -> Optional[dict]:
    return await employees_collection.find_one({"telegram_id": telegram_id})


# ---------- JOBS ----------

async def create_job(
    company_id: ObjectIdLike,
    employee_id: ObjectIdLike,
    description: str,
    location: str | None = None,
    due_at: datetime | None = None,
) -> dict:
    company_oid = _to_object_id(company_id)
    employee_oid = _to_object_id(employee_id)

    doc = {
        "company_id": company_oid,
        "employee_id": employee_oid,
        "description": description,
        "location": location,
        "due_at": due_at,  # currently None (we’ll improve parsing later)
        "status": "open",
        "created_at": datetime.utcnow(),
    }

    result = await jobs_collection.insert_one(doc)
    doc["_id"] = result.inserted_id
    return doc
