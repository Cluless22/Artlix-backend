from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.domain.repositories import (
    create_company,
    get_company_by_owner,
    create_employee,
)
from app.domain.models import UserRole

router = Router()


@router.message(Command("owner_setup"))
async def owner_setup(message: Message) -> None:
    """
    Owner creates a company and gets an office code to share with employees.

    Usage:
        /owner_setup My Company Name
    """
    from_user = message.from_user
    owner_tg_id = from_user.id

    # Check if owner already has a company
    existing_company = await get_company_by_owner(owner_tg_id)
    if existing_company:
        await message.answer(
            "✅ You already have a company set up.\n\n"
            f"🏢 <b>{existing_company.title}</b>\n"
            f"🔑 Office code: <code>{existing_company.office_code}</code>\n\n"
            "Share this code with employees so they can join using:\n"
            "<code>/join_company "
            f"{existing_company.office_code} Their Name</code>"
        )
        return

    # Parse company name from command text
    # Expect: "/owner_setup My Company Name"
    parts = (message.text or "").split(maxsplit=1)
    if len(parts) < 2:
        await message.answer(
            "To set up your company, use:\n"
            "<code>/owner_setup My Company Name</code>"
        )
        return

    company_title = parts[1].strip()

    company = await create_company(
        owner_telegram_id=owner_tg_id,
        title=company_title,
    )

    # Also create the owner as an employee record
    owner_name = from_user.full_name or from_user.username or "Owner"

    owner_employee = await create_employee(
        company_id=company.id,
        name=owner_name,
        telegram_id=owner_tg_id,
        role=UserRole.OWNER,
    )

    await message.answer(
        "✅ Company created!\n\n"
        f"🏢 <b>{company.title}</b>\n"
        f"👑 Owner: {owner_employee.name}\n"
        f"🔑 Office code (share with your team): "
        f"<code>{company.office_code}</code>\n\n"
        "Employees join with:\n"
        f"<code>/join_company {company.office_code} Their Name</code>\n\n"
        "After they join, they can send me job requests as plain text."
    )
