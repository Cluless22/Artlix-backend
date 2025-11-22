import httpx
from app.core.config import get_settings
from app.domain.models import Job

settings = get_settings()


async def trigger_job_created(job: Job):
    """
    Trigger n8n workflow for:
    - Google Sheets tracking
    - Calendar sync
    - follow-up automation
    """
    url = f"{settings.N8N_BASE_URL}/webhook/job-created/{settings.N8N_WEBHOOK_SECRET}"

    payload = {
        "job_id": job.id,
        "company_id": job.company_id,
        "created_by_employee_id": job.created_by_employee_id,
        "client_name": job.client_name,
        "job_type": job.job_type,
        "location": job.location,
        "scheduled_for": job.scheduled_for.isoformat() if job.scheduled_for else None,
        "budget": job.budget,
        "notes": job.notes,
        "status": job.status,
    }

    async with httpx.AsyncClient(timeout=10) as client:
        try:
            await client.post(url, json=payload)
        except Exception as e:
            print("[n8n] job-created error:", e)
