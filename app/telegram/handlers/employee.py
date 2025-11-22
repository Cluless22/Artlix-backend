from aiogram import Router, F
from aiogram.types import Message

from app.domain.repositories import (
    get_company_by_office_code,
    create_employee,
    get_employee_by_telegram_id,
)
from app.domain.decision_engine import classify_message, Intent
from app.domain.workflows.job_intake import handle_job_intake
from app.telegram.bot import bot

router = Router()


@router.message(F.text.startswith("/join"))
async def cmd_join(message: Message):
    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("Usage: /join <office_code>\nAsk your boss for the code.")
        return

    office_code = parts[1].strip()
    company = await get_company_by_office_code(office_code)
    if not company:
        await message.answer("❌ That office code is invalid. Double-check with your boss.")
        return

    existing = await get_employee_by_telegram_id(message.from_user.id)
    if existing:
        await message.answer("You're already linked to a company. You're good to go 🚀")
        return

    await create_employee(
        telegram_id=message.from_user.id,
        company_id=company.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
    )

    await message.answer(
        f"✅ You're now linked to <b>{company.title}</b>.\n"
        "Just describe jobs in natural language (e.g. “New job: kitchen reno for John…”) "
        "and I'll capture them + notify your boss."
    )


@router.message(F.chat.type == "private")
async def employee_message(message: Message):
    employee = await get_employee_by_telegram_id(message.from_user.id)

    if not employee:
        await message.answer(
            "I don't know which company you're with yet.\n"
            "Ask your boss for the office code and send: /join <office_code>"
        )
        return

    intent = classify_message(message.text or "")

    if intent == Intent.JOB_INTAKE:
        await handle_job_intake(bot, message.from_user.id, message.text)
    else:
        await message.answer(
            "Got it. Right now I'm best at capturing new jobs.\n"
            "Try including words like 'new job', 'lead', 'estimate', or 'quote'."
        )
