from typing import Optional
from bson import ObjectId

from app.infrastructure.db import companies_collection, employees_collection, jobs_collection
from app.domain.models import Company, Employee, Job


def _to_str_id(doc: dict | None):
    if not doc:
        return None
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc


# COMPANY

async def create_company(owner_telegram_id: int, title: str, office_code: str) -> Company:
    col = companies_collection()
    doc = {
        "owner_telegram_id": owner_telegram_id,
        "title": title,
        "office_code": office_code,
    }
    res = await col.insert_one(doc)
    doc["_id"] = res.inserted_id
    return Company(**_to_str_id(doc))


async def get_company_by_office_code(code: str) -> Optional[Company]:
    col = companies_collection()
    doc = await col.find_one({"office_code": code})
    if not doc:
        return None
    return Company(**_to_str_id(doc))


async def get_company_by_owner(telegram_id: int) -> Optional[Company]:
    col = companies_collection()
    doc = await col.find_one({"owner_telegram_id": telegram_id})
    if not doc:
        return None
    return Company(**_to_str_id(doc))


async def get_company_by_id(company_id: str) -> Optional[Company]:
    col = companies_collection()
    try:
        oid = ObjectId(company_id)
    except Exception:
        return None
    doc = await col.find_one({"_id": oid})
    if not doc:
        return None
    return Company(**_to_str_id(doc))


# EMPLOYEE

async def create_employee(
    telegram_id: int,
    company_id: str,
    username: str | None,
    first_name: str | None,
    last_name: str | None,
) -> Employee:
    col = employees_collection()
    doc = {
        "telegram_id": telegram_id,
        "username": username,
        "first_name": first_name,
        "last_name": last_name,
        "company_id": company_id,
    }
    res = await col.insert_one(doc)
    doc["_id"] = res.inserted_id
    return Employee(**_to_str_id(doc))


async def get_employee_by_telegram_id(telegram_id: int) -> Optional[Employee]:
    col = employees_collection()
    doc = await col.find_one({"telegram_id": telegram_id})
    if not doc:
        return None
    return Employee(**_to_str_id(doc))


# JOB

async def create_job(job: Job) -> Job:
    col = jobs_collection()
    doc = job.model_dump(by_alias=True, exclude_none=True)
    if "_id" in doc and doc["_id"]:
        doc["_id"] = ObjectId(doc["_id"])
    res = await col.insert_one(doc)
    doc["_id"] = res.inserted_id
    return Job(**_to_str_id(doc))
