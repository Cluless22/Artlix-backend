import re
from datetime import datetime, timedelta
from typing import Optional


class ParsedJob:
    def __init__(
        self,
        client_name: Optional[str] = None,
        job_type: Optional[str] = None,
        location: Optional[str] = None,
        scheduled_for: Optional[datetime] = None,
        budget: Optional[float] = None,
        notes: Optional[str] = None,
    ):
        self.client_name = client_name
        self.job_type = job_type
        self.location = location
        self.scheduled_for = scheduled_for
        self.budget = budget
        self.notes = notes


def parse_job_intake(text: str) -> ParsedJob:
    t = text.strip()

    client_match = re.search(r"(client|name)\s*[:\-]\s*(.+?)(?:,|\n|$)", t, re.IGNORECASE)
    client_name = client_match.group(2).strip() if client_match else None

    job_match = re.search(r"(job|for)\s*[:\-]?\s*(.+?)(?:,|\n|$)", t, re.IGNORECASE)
    job_type = job_match.group(2).strip() if job_match else None

    loc_match = re.search(r"(address|at)\s*[:\-]?\s*(.+?)(?:,|\n|$)", t, re.IGNORECASE)
    location = loc_match.group(2).strip() if loc_match else None

    budget_match = re.search(r"(\d+(?:\.\d+)?)\s*(k|K|thousand|\$)", t)
    budget = None
    if budget_match:
        num = float(budget_match.group(1))
        if budget_match.group(2).lower() in ("k", "thousand"):
            num *= 1000
        budget = num

    scheduled_for = None
    now = datetime.utcnow()
    tl = t.lower()
    if "tomorrow" in tl:
        scheduled_for = now + timedelta(days=1)
    elif "next week" in tl:
        scheduled_for = now + timedelta(days=7)

    notes = t

    return ParsedJob(
        client_name=client_name,
        job_type=job_type,
        location=location,
        scheduled_for=scheduled_for,
        budget=budget,
        notes=notes,
    )
