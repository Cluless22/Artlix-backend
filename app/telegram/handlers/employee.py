from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.domain.repositories import (
    get_company_by_code,
    get_or_create_employee_by_telegram,
    create_job,
)
from app.telegram.decision_engine import classify_message_and_build_job

router = Router()


@router.message(Command("join_company"))
async def join_company(message: Message) -> None:
    """
    Employee runs: /join_company <company_code>
    This links their Telegram account to a company.
    """
    parts = message.text.split()
    if len(parts) < 2:
        await message.answer(
            "Usage:\n"
            "/join_company <company_code>\n\n"
            "Ask your boss for the code."
        )
        return

    code = parts[1].strip()
    company = await get_company_by_code(code)

    if not company:
        await message.answer("❌ I couldn't find a company with that code.")
        return

    employee = await get_or_create_employee_by_telegram(
        company_id=company.id,
        telegram_id=message.from_user.id,
        name=message.from_user.full_name or "Employee",
    )

    await message.answer(
        "✅ You're now linked to the company:\n"
        f"🏢 <b>{company.name}</b>\n\n"
        "Now you can send me job details in this chat, like:\n"
        "<i>New driveway pour for Smith, Thursday 9am, address 123 Main St.</i>"
    )


@router.message()
async def handle_employee_message(message: Message) -> None:
    """
    Handles general employee messages in private chat.
    For now we treat any free text as a potential job description.
    """
    classification = classify_message_and_build_job(message.text)

    if not classification.is_job:
        await message.answer(
            "🤖 I see your message, but I'm not sure it's a job yet.\n"
            "Try something like:\n"
            "<i>Concrete pour for Johnson at 9am tomorrow, 15 King St.</i>"
        )
        return

    job = await create_job(
        company_id=classification.company_id,  # TODO: fill from employee's company
        created_by_telegram_id=message.from_user.id,
        title=classification.title,
        description=classification.description,
        scheduled_for=classification.scheduled_for,
        client_name=classification.client_name,
        location=classification.location,
        raw_text=message.text,
    )

    await message.answer(
        "✅ Job captured!\n\n"
        f"📋 <b>{job.title}</b>\n"
        f"👤 Client: {job.client_name or 'N/A'}\n"
        f"📍 Location: {job.location or 'N/A'}\n"
        f"🗓 When: {job.scheduled_for or 'unscheduled'}\n\n"
        "I'll soon sync this to your job tracking sheet and notify the owner."
    )
