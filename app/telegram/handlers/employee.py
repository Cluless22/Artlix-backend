from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.domain.repositories import (
    get_company_by_code,
    get_or_create_employee_by_telegram,
    get_employee_by_telegram,
    create_job,
)
from app.telegram.decision_engine import classify_message_and_build_job

router = Router()


@router.message(Command("join_company"))
async def join_company(message: Message) -> None:
    """
    Employees join a company using the office code shared by the owner.

    Usage:
        /join_company OFFICE_CODE Your Name
    """
    parts = (message.text or "").split(maxsplit=2)
    if len(parts) < 3:
        await message.answer(
            "To join a company, use:\n"
            "<code>/join_company OFFICE_CODE Your Name</code>"
        )
        return

    office_code = parts[1].strip().upper()
    employee_name = parts[2].strip()

    company = await get_company_by_code(office_code)
    if not company:
        await message.answer(
            "❌ I couldn't find a company with that office code.\n"
            "Double-check the code with your owner."
        )
        return

    employee = await get_or_create_employee_by_telegram(
        company_id=company.id,
        telegram_id=message.from_user.id,
        name=employee_name,
    )

    await message.answer(
        "✅ You’re now linked to this company.\n\n"
        f"🏢 <b>{company.title}</b>\n"
        f"👷 Employee: {employee.name}\n\n"
        "Now just send me job requests as text (who / what / where / when), "
        "and I’ll capture them as jobs."
    )


@router.message()
async def capture_job(message: Message) -> None:
    """
    Default handler for non-command messages from employees:
    tries to classify and store them as jobs.
    """
    text = message.text or ""

    if text.startswith("/"):
        return

    employee = await get_employee_by_telegram(telegram_id=message.from_user.id)
    if not employee:
        await message.answer(
            "I don't know which company you're in yet.\n\n"
            "Ask your owner for the office code, then run:\n"
            "<code>/join_company OFFICE_CODE Your Name</code>"
        )
        return

    classification = classify_message_and_build_job(text)
    if not classification.is_job:
        await message.answer(
            "I couldn't understand this as a job yet.\n"
            "Try sending something like:\n"
            "<i>\"Pouring concrete for John at 123 Main on Friday morning\"</i>"
        )
        return

    job = await create_job(
        company_id=employee.company_id,
        employee_id=employee.id,
        title=classification.title,
        description=classification.description,
        scheduled_for=classification.scheduled_for,
        client_name=classification.client_name,
        location=classification.location,
        raw_text=text,
    )

    when_str = job.scheduled_for.isoformat() if job.scheduled_for else "unscheduled"

    await message.answer(
        "✅ Job captured!\n\n"
        f"📋 <b>{job.job_type}</b>\n"
        f"👤 Client: {job.client_name or 'N/A'}\n"
        f"📍 Location: {job.location or 'N/A'}\n"
        f"🗓 When: {when_str}\n\n"
        "Soon I'll sync this to your job tracking sheet and notify the owner."
    )
