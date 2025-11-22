from enum import Enum


class Intent(str, Enum):
    JOB_INTAKE = "job_intake"
    SCHEDULING = "scheduling"
    FOLLOW_UP = "follow_up"
    DAILY_DIGEST = "daily_digest"
    UNKNOWN = "unknown"


def classify_message(text: str) -> Intent:
    t = (text or "").lower()

    keywords_job = ["new job", "job:", "lead", "estimate", "quote", "renovation", "reno"]
    keywords_schedule = ["schedule", "book", "appointment", "site visit"]
    keywords_follow = ["follow up", "follow-up", "check in", "status update"]
    keywords_digest = ["daily report", "digest", "summary of today"]

    if any(k in t for k in keywords_job):
        return Intent.JOB_INTAKE
    if any(k in t for k in keywords_schedule):
        return Intent.SCHEDULING
    if any(k in t for k in keywords_follow):
        return Intent.FOLLOW_UP
    if any(k in t for k in keywords_digest):
        return Intent.DAILY_DIGEST
    return Intent.UNKNOWN
