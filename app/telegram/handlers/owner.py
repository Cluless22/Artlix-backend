from aiogram import Router, F
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
    Owner runs this in a private chat to register their company.
    For now, we use their Telegram user id as the owner id.
    """
    owner_tg_id = message.from_user.id

    # Check if this owner already has a company
    existing = await get_company_by_owner(owner_tg_id)
    if existing:
        await message.answer(
            f"✅ You already have a company registered:\n"
            f"🏢 <b>{existing.name}</b>\n"
            f"Company code: <code>{existing.code}</code>\n\n"
            f"Share this code with employees so they can join."
        )
        return

    # Simple stub company name for now - later we'll ask for it interactively
    company_name = f"{message.from_user.full_name}'s Company"

    company = await create_company(
        owner_telegram_id=owner_tg_id,
        name=company_name,
    )

    await message.answer(
        "🏢 Company created!\n\n"
        f"Name: <b>{company.name}</b>\n"
        f"Company code: <code>{company.code}</code>\n\n"
        "👷 Share this code with your employees.\n"
        "They will use /join_company <code> to connect."
    )


@router.message(Command("create_employee"))
async def create_employee_manual(message: Message) -> None:
    """
    Temporary helper: owner can create an employee record manually.
    Later, employees will self-join using /join_company <code>.
    Usage: /create_employee John 123456789
    """
    parts = message.text.split()
    if len(parts) < 3:
        await message.answer(
            "Usage:\n"
            "/create_employee <name> <employee_telegram_id>\n\n"
            "Example:\n"
            "/create_employee John 123456789"
        )
        return

    owner_tg_id = message.from_user.id
    name = parts[1]
    try:
        employee_tg_id = int(parts[2])
    except ValueError:
        await message.answer("❌ employee_telegram_id must be a number.")
        return

    company = await get_company_by_owner(owner_tg_id)
    if not company:
        await message.answer(
            "❌ You don't have a company yet.\n"
            "Run /owner_setup first."
        )
        return

    employee = await create_employee(
        company_id=company.id,
        name=name,
        telegram_id=employee_tg_id,
        role=UserRole.EMPLOYEE,
    )

    await message.answer(
        f"✅ Employee created:\n"
        f"👷 {employee.name}\n"
        f"Telegram id: <code>{employee.telegram_id}</code>\n"
        f"Company: <b>{company.name}</b>"
    )
