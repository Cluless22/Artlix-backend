from datetime import datetime
from typing import Optional, Any
from enum import Enum

from pydantic import BaseModel, Field


class UserRole(str, Enum):
    OWNER = "owner"
    EMPLOYEE = "employee"


class Company(BaseModel):
    # Use Any so Mongo ObjectId doesn't break validation
    id: Optional[Any] = Field(default=None, alias="_id")
    owner_telegram_id: int
    title: str
    office_code: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @property
    def name(self) -> str:
        # convenience so we can use company.name
        return self.title


class Employee(BaseModel):
    id: Optional[Any] = Field(default=None, alias="_id")
    company_id: Any
    telegram_id: int
    name: Optional[str] = None
    role: UserRole = UserRole.EMPLOYEE
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Job(BaseModel):
    id: Optional[Any] = Field(default=None, alias="_id")
    company_id: Any
    created_by_employee_id: Any

    client_name: Optional[str] = None
    job_type: Optional[str] = None
    location: Optional[str] = None
    scheduled_for: Optional[datetime] = None
    budget: Optional[float] = None
    notes: Optional[str] = None

    raw_text: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = "new"
