from datetime import datetime
from typing import Optional, Union

from bson import ObjectId

from app.domain.models import Company, Employee, Job, UserRole
from app.infrastructure.db import (
    companies_collection,
    employees_collection,
    jobs_collection,
)

ObjectIdLike = Union[str, ObjectId]


def _to_object_id(value: ObjectIdLike) -> ObjectId:
    """
    Accept either a string or ObjectId and always return an ObjectId.
    """
    if isinstance(value, ObjectId):
        return value
    return ObjectId(str(value))


# ---------------------------------------------------------------------------
# Company helpers
# ---------------------------------------------------------------------------

async def create_company(
    *,
    owner_telegram_id: int,
    title: str,
    office_code: str,
) -> Company:
    doc = {
        "owner_telegram_id": owner_telegram_id,
        "title": title,
        "office_code": office_code,
        "created_at": datetime.utcnow(),
    }
    result = await companies_collection.insert_one(doc)
    doc["_id"] = result.inserted_id
    return Company.model_validate(doc)


async def get_company_by_owner(owner_telegram_id: int) -> Optional[Company]:
    doc = await companies_collection.find_one({"owner_telegram_id": owner_telegram_id})
    if not doc:
        return None
    return Company.model_validate(doc)


async def get_company_by_code(office_code: str) -> Optional[Company]:
    doc = await companies_collection.find_one({"office_code": office_code})
    if not doc:
        return None
    return Company.model_validate(doc)


# ---------------------------------------------------------------------------
# Employee helpers
# ---------------------------------------------------------------------------

async def create_employee(
    *,
    company_id: ObjectIdLike,
    name: str,
    telegram_id: int,
    role: UserRole,
) -> Employee:
    company_oid = _to_object_id(company_id)

    doc = {
        "company_id": company_oid,
        "name": name,
        "telegram_id": telegram_id,
        "role": role.value if hasattr(role, "value") else str(role),
        "created_at": datetime.utcnow(),
    }

    result = await employees_collection.insert_one(doc)
    doc["_id"] = result.inserted_id
    return Employee.model_validate(doc)


async def get_or_create_employee_by_telegram(
    *,
    company_id: ObjectIdLike,
    telegram_id: int,
    name: Optional[str] = None,
    role: Optional[UserRole] = None,
) -> Employee:
    company_oid = _to_object_id(company_id)

    existing = await employees_collection.find_one(
        {"company_id": company_oid, "telegram_id": telegram_id}
    )
    if existing:
        return Employee.model_validate(existing)

    doc = {
        "company_id": company_oid,
        "telegram_id": telegram_id,
        "name": name or "Unknown",
        "role": (
            role.value if (role and hasattr(role, "value"))
            else (str(role) if role else "employee")
        ),
        "created_at": datetime.utcnow(),
    }

    result = await employees_collection.insert_one(doc)
    doc["_id"] = result.inserted_id
    return Employee.model_validate(doc)


# ---------------------------------------------------------------------------
# Job helpers
# ---------------------------------------------------------------------------

async def create_job(
    *,
    company_id: ObjectIdLike,
    employee_id: ObjectIdLike,
    title: str,
    description: str,
    scheduled_for: Optional[datetime] = None,
    client_name: Optional[str] = None,
    location: Optional[str] = None,
    budget: Optional[float] = None,
    notes: Optional[str] = None,
    raw_text: str,
) -> Job:
    company_oid = _to_object_id(company_id)
    employee_oid = _to_object_id(employee_id)

    doc = {
        "company_id": company_oid,
        "created_by_employee_id": employee_oid,
        "title": title,
        "description": description,
        "scheduled_for": scheduled_for,
        "client_name": client_name,
        "location": location,
        "budget": budget,
        "notes": notes,
        "raw_text": raw_text,
        "created_at": datetime.utcnow(),
        "status": "new",
    }

    result = await jobs_collection.insert_one(doc)
    doc["_id"] = result.inserted_id
    return Job.model_validate(doc)
