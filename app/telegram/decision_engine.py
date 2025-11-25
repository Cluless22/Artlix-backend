from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class JobClassificationResult:
    is_job: bool
    title: str = ""
    description: str = ""
    scheduled_for: Optional[datetime] = None
    client_name: Optional[str] = None
    location: Optional[str] = None
    company_id: Optional[str] = None


def classify_message_and_build_job(text: str) -> JobClassificationResult:
    """
    SUPER simple placeholder:

    - If message is too short, treat it as non-job.
    - Otherwise treat the whole text as job description.
    """
    if not text:
        return JobClassificationResult(is_job=False)

    cleaned = text.strip()

    if len(cleaned) < 15:
        return JobClassificationResult(is_job=False)

    return JobClassificationResult(
        is_job=True,
        title="New job",
        description=cleaned,
        scheduled_for=None,
        client_name=None,
        location=None,
        company_id=None,
    )
