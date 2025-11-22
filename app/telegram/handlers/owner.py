import secrets
from aiogram import Router, F
from aiogram.types import Message, ChatType

from app.domain.repositories import create_company, get_company_by_owner

router = Router()


def _generate_office_code() -> str:
    return secrets.token_hex(3).upper()


@router.message(
    F.text == "/setup",
    F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP})
)
async def cmd_setup(message: Message):
    owner_id = message.from_user.id
    chat_title = message.chat.title or "Unnamed Company"

    existing = await get_company_by_owner(owner_id)
    if existing:
        await message.reply(
            "✅ Your company is already set up.\n"
            f"Office code: <code>{existing.office_code}</code>\n"
            "Share this code with your employees so they can DM me with /join."
        )
        return

    office_code = _generate_office_code()
    company = await create_company(
        owner_telegram_id=owner_id,
        title=chat_title,
        office_code=office_code,
    )

    await message.reply(
        f"✅ Company created: <b>{company.title}</b>\n\n"
        f"Office code: <code>{company.office_code}</code>\n"
        "1️⃣ Share this code with your employees.\n"
        "2️⃣ They DM me with: /join OFFICE_CODE\n"
        "3️⃣ They send jobs, and I'll notify you automatically."
    )
