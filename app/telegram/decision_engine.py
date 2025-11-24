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
    company_id: Optional[str] = None  # we'll fill this once we attach employee->company lookup


def classify_message_and_build_job(text: str) -> JobClassificationResult:
    """
    Super simple starter 'decision engine'.

    Later this will:
    - use NLP / LLM
    - detect intents (job, schedule change, status update, etc.)
    - extract entities (date, time, client, address)

    For now:
    - if text is short, we say it's not a job
    - otherwise we treat it as a job with the whole text as description.
    """
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
