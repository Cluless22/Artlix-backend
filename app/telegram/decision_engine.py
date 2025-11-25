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
    company_id: Optional[str] = None  # reserved for future use


def classify_message_and_build_job(text: str) -> JobClassificationResult:
    """
    VERY simple placeholder "classifier":
    - If message is short, we treat it as non-job
    - Otherwise we mark it as a generic job with the raw text
    """
    cleaned = (text or "").strip()

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
