from fastapi import APIRouter, HTTPException
from aiogram.types import Update

from app.telegram.bot import bot
from app.domain.repositories import (
    create_company,
    get_company_by_owner,
    get_companies_by_owner,
    create_employee,
    get_company_by_code,
    get_or_create_employee_by_telegram,
    get_employee_by_telegram,
    delete_employee_by_telegram,
    delete_company_and_related,
    create_job,
)
from app.domain.models import UserRole
from app.telegram.decision_engine import classify_message_and_build_job

router = APIRouter()


@router.post("/telegram/webhook")
async def telegram_webhook(update: dict):
    """
    Telegram sends all updates here as JSON.

    Directly handle bot logic:

      • /start
      • /owner_setup My Company Name
      • /new_company My Other Company
      • /my_companies
      • /delete_company OFFICE_CODE
      • /join_company OFFICE_CODE Your Name
      • /leave_company
      • any other text → try to capture as a job
    """
    print("[telegram_webhook] incoming update:", update)

    # --- 1) Validate the update into an aiogram Update object ---
    try:
        tg_update = Update.model_validate(update)
    except Exception as e:
        print("[telegram_webhook] bad update:", repr(e))
        raise HTTPException(status_code=400, detail="Invalid Telegram update")

    msg = tg_update.message or tg_update.edited_message
    if not msg or msg.from_user is None or msg.from_user.is_bot:
        # Nothing we can respond to
        return {"ok": True}

    chat_id = msg.chat.id
    text = (msg.text or "").strip()
    from_user = msg.from_user

    try:
        # --- 2) /start ---
        if text.startswith("/start"):
            await bot.send_message(
                chat_id=chat_id,
                text=(
                    "👋 Hey! I'm Artlix.\n\n"
                    "I help construction teams capture jobs, schedule work,\n"
                    "and keep owners in the loop.\n\n"
                    "Getting started:\n"
                    "• Owners: /owner_setup My Company Name\n"
                    "• Employees: /join_company OFFICE_CODE Your Name\n\n"
                    "Extra owner commands:\n"
                    "• /my_companies\n"
                    "• /new_company Another Company Name\n"
                    "• /delete_company OFFICE_CODE\n"
                    "Employees can leave with:\n"
                    "• /leave_company"
                ),
            )
            return {"ok": True}

        # --- 3) /owner_setup My Company Name ---
        if text.startswith("/owner_setup"):
            parts = text.split(maxsplit=1)
            owner_tg_id = from_user.id

            # If already has a company, show info + hint for /my_companies & /new_company
            existing = await get_company_by_owner(owner_tg_id)
            if existing:
                await bot.send_message(
                    chat_id=chat_id,
                    text=(
                        "✅ You already have at least one company set up.\n\n"
                        f"Example:\n"
                        f"🏢 <b>{existing.title}</b>\n"
                        f"🔑 Office code: <code>{existing.office_code}</code>\n\n"
                        "You can see all your companies with:\n"
                        "<code>/my_companies</code>\n\n"
                        "You can create a new one with:\n"
                        "<code>/new_company Another Company Name</code>"
                    ),
                )
                return {"ok": True}

            if len(parts) < 2:
                await bot.send_message(
                    chat_id=chat_id,
                    text=(
                        "To set up your first company, use:\n"
                        "<code>/owner_setup My Company Name</code>"
                    ),
                )
                return {"ok": True}

            company_title = parts[1].strip()

            company = await create_company(
                owner_telegram_id=owner_tg_id,
                title=company_title,
            )

            owner_name = (
                from_user.full_name
                or from_user.username
                or "Owner"
            )

            owner_employee = await create_employee(
                company_id=company.id,
                name=owner_name,
                telegram_id=owner_tg_id,
                role=UserRole.OWNER,
            )

            await bot.send_message(
                chat_id=chat_id,
                text=(
                    "✅ Company created!\n\n"
                    f"🏢 <b>{company.title}</b>\n"
                    f"👑 Owner: {owner_employee.name}\n"
                    f"🔑 Office code (share with your team): "
                    f"<code>{company.office_code}</code>\n\n"
                    "Employees join with:\n"
                    f"<code>/join_company {company.office_code} Their Name</code>\n\n"
                    "You can create more companies later with:\n"
                    "<code>/new_company Another Company Name</code>"
                ),
            )
            return {"ok": True}

        # --- 4) /new_company Another Company Name ---
        if text.startswith("/new_company"):
            parts = text.split(maxsplit=1)
            owner_tg_id = from_user.id

            if len(parts) < 2:
                await bot.send_message(
                    chat_id=chat_id,
                    text=(
                        "To create a new company, use:\n"
                        "<code>/new_company Another Company Name</code>"
                    ),
                )
                return {"ok": True}

            company_title = parts[1].strip()

            company = await create_company(
                owner_telegram_id=owner_tg_id,
                title=company_title,
            )

            owner_name = (
                from_user.full_name
                or from_user.username
                or "Owner"
            )

            # Create owner employee for this new company as well
            owner_employee = await create_employee(
                company_id=company.id,
                name=owner_name,
                telegram_id=owner_tg_id,
                role=UserRole.OWNER,
            )

            await bot.send_message(
                chat_id=chat_id,
                text=(
                    "✅ New company created!\n\n"
                    f"🏢 <b>{company.title}</b>\n"
                    f"👑 Owner: {owner_employee.name}\n"
                    f"🔑 Office code (share with your team): "
                    f"<code>{company.office_code}</code>\n\n"
                    "Employees join with:\n"
                    f"<code>/join_company {company.office_code} Their Name</code>\n\n"
                    "See all your companies with:\n"
                    "<code>/my_companies</code>"
                ),
            )
            return {"ok": True}

        # --- 5) /my_companies ---
        if text.startswith("/my_companies"):
            owner_tg_id = from_user.id
            companies = await get_companies_by_owner(owner_tg_id)

            if not companies:
                await bot.send_message(
                    chat_id=chat_id,
                    text=(
                        "You don't own any companies yet.\n\n"
                        "Create one with:\n"
                        "<code>/owner_setup My Company Name</code>"
                    ),
                )
                return {"ok": True}

            lines = ["📋 <b>Your companies:</b>"]
            for c in companies:
                lines.append(
                    f"• {c.title} — code: <code>{c.office_code}</code>"
                )

            lines.append(
                "\nDelete one with:\n"
                "<code>/delete_company OFFICE_CODE</code>"
            )

            await bot.send_message(
                chat_id=chat_id,
                text="\n".join(lines),
            )
            return {"ok": True}

        # --- 6) /delete_company OFFICE_CODE ---
        if text.startswith("/delete_company"):
            parts = text.split(maxsplit=1)
            if len(parts) < 2:
                await bot.send_message(
                    chat_id=chat_id,
                    text=(
                        "To delete a company, use:\n"
                        "<code>/delete_company OFFICE_CODE</code>"
                    ),
                )
                return {"ok": True}

            code = parts[1].strip().upper()
            company = await get_company_by_code(code)
            if not company:
                await bot.send_message(
                    chat_id=chat_id,
                    text="❌ I couldn't find a company with that office code.",
                )
                return {"ok": True}

            # Only the owner of that company can delete it
            if company.owner_telegram_id != from_user.id:
                await bot.send_message(
                    chat_id=chat_id,
                    text=(
                        "❌ You are not the owner of this company, "
                        "so you can't delete it."
                    ),
                )
                return {"ok": True}

            deleted_count = await delete_company_and_related(company.id)
            if deleted_count == 0:
                await bot.send_message(
                    chat_id=chat_id,
                    text="Something went wrong while deleting that company.",
                )
                return {"ok": True}

            await bot.send_message(
                chat_id=chat_id,
                text=(
                    "🗑️ Company deleted.\n\n"
                    f"🏢 <b>{company.title}</b>\n"
                    f"🔑 Code: <code>{company.office_code}</code>\n\n"
                    "All employees and jobs linked to this company were removed."
                ),
            )
            return {"ok": True}

        # --- 7) /join_company OFFICE_CODE Your Name ---
        if text.startswith("/join_company"):
            parts = text.split(maxsplit=2)
            if len(parts) < 3:
                await bot.send_message(
                    chat_id=chat_id,
                    text=(
                        "To join a company, use:\n"
                        "<code>/join_company OFFICE_CODE Your Name</code>"
                    ),
                )
                return {"ok": True}

            office_code = parts[1].strip().upper()
            employee_name = parts[2].strip()

            company = await get_company_by_code(office_code)
            if not company:
                await bot.send_message(
                    chat_id=chat_id,
                    text=(
                        "❌ I couldn't find a company with that office code.\n"
                        "Double-check the code with your owner."
                    ),
                )
                return {"ok": True}

            employee = await get_or_create_employee_by_telegram(
                company_id=company.id,
                telegram_id=from_user.id,
                name=employee_name,
            )

            await bot.send_message(
                chat_id=chat_id,
                text=(
                    "✅ You’re now linked to this company.\n\n"
                    f"🏢 <b>{company.title}</b>\n"
                    f"👷 Employee: {employee.name}\n\n"
                    "Now just send me job requests as text (who / what / where / when), "
                    "and I’ll capture them as jobs.\n\n"
                    "If you ever need to leave, use:\n"
                    "<code>/leave_company</code>"
                ),
            )
            return {"ok": True}

        # --- 8) /leave_company ---
        if text.startswith("/leave_company"):
            deleted = await delete_employee_by_telegram(from_user.id)
            if deleted == 0:
                await bot.send_message(
                    chat_id=chat_id,
                    text=(
                        "You are not currently linked to any company.\n\n"
                        "To join one, use:\n"
                        "<code>/join_company OFFICE_CODE Your Name</code>"
                    ),
                )
                return {"ok": True}

            await bot.send_message(
                chat_id=chat_id,
                text=(
                    "✅ You have left your company.\n\n"
                    "If you want to join another company later, use:\n"
                    "<code>/join_company OFFICE_CODE Your Name</code>"
                ),
            )
            return {"ok": True}

        # --- 9) Any other text → treat as job from an employee ---
        employee = await get_employee_by_telegram(telegram_id=from_user.id)
        if not employee:
            await bot.send_message(
                chat_id=chat_id,
                text=(
                    "I don't know which company you're in yet.\n\n"
                    "Ask your owner for the office code, then run:\n"
                    "<code>/join_company OFFICE_CODE Your Name</code>"
                ),
            )
            return {"ok": True}

        classification = classify_message_and_build_job(text)
        if not classification.is_job:
            await bot.send_message(
                chat_id=chat_id,
                text=(
                    "I couldn't understand this as a job yet.\n"
                    "Try sending something like:\n"
                    "<i>\"Pouring concrete for John at 123 Main on Friday morning\"</i>"
                ),
            )
            return {"ok": True}

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

        await bot.send_message(
            chat_id=chat_id,
            text=(
                "✅ Job captured!\n\n"
                f"📋 <b>{job.job_type}</b>\n"
                f"👤 Client: {job.client_name or 'N/A'}\n"
                f"📍 Location: {job.location or 'N/A'}\n"
                f"🗓 When: {when_str}\n\n"
                "Soon I'll sync this to your job tracking sheet and notify the owner."
            ),
        )

    except Exception as e:
        # Don't let the whole webhook crash
        print("[telegram_webhook] error while handling update:", repr(e))

    return {"ok": True}
