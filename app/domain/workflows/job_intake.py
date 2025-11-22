from aiogram import Bot

from app.domain.models import Job
from app.domain.repositories import (
    create_job,
    get_employee_by_telegram_id,
    get_company_by_id,
)
from app.domain.nlp.parser import parse_job_intake
from app.infrastructure.n8n_client import trigger_job_created


async def handle_job_intake(bot: Bot, telegram_user_id: int, text: str):
    employee = await get_employee_by_telegram_id(telegram_user_id)
    if not employee:
        await bot.send_message(
            chat_id=telegram_user_id,
            text="I couldn't find your company link. Send /join <office_code> first."
        )
        return

    parsed = parse_job_intake(text)

    job = Job(
        company_id=employee.company_id,
        created_by_employee_id=employee.id,
        client_name=parsed.client_name,
        job_type=parsed.job_type,
        location=parsed.location,
        scheduled_for=parsed.scheduled_for,
        budget=parsed.budget,
        notes=parsed.notes,
        raw_text=text,
    )

    job = await create_job(job)

    await trigger_job_created(job)

    confirm_msg = (
        "✅ Job captured!\n\n"
        f"<b>Client:</b> {job.client_name or 'N/A'}\n"
        f"<b>Job:</b> {job.job_type or 'N/A'}\n"
        f"<b>Location:</b> {job.location or 'N/A'}\n"
        f"<b>Budget:</b> {job.budget or 'N/A'}\n"
    )
    await bot.send_message(chat_id=telegram_user_id, text=confirm_msg)

    company = await get_company_by_id(job.company_id)
    if company:
        owner_text = (
            "📥 <b>New job added</b>\n\n"
            f"From employee ID: <code>{employee.telegram_id}</code>\n"
            f"Client: {job.client_name or 'N/A'}\n"
            f"Job: {job.job_type or 'N/A'}\n"
            f"Location: {job.location or 'N/A'}\n"
            f"Budget: {job.budget or 'N/A'}\n"
        )
        try:
            await bot.send_message(chat_id=company.owner_telegram_id, text=owner_text)
        except Exception as e:
            print("[owner notify] error:", e)
