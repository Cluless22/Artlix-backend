from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Company(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    owner_telegram_id: int
    title: str
    office_code: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Employee(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    telegram_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Job(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    company_id: str
    created_by_employee_id: str

    client_name: Optional[str] = None
    job_type: Optional[str] = None
    location: Optional[str] = None
    scheduled_for: Optional[datetime] = None
    budget: Optional[float] = None
    notes: Optional[str] = None

    raw_text: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = "new"
