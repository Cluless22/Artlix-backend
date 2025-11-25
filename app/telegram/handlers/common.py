from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(
        "👋 Hey! I'm Artlix.\n\n"
        "I help construction teams capture jobs, schedule work,\n"
        "and keep owners in the loop.\n\n"
        "Getting started:\n"
        "• Owners: /owner_setup My Company Name\n"
        "• Employees: /join_company OFFICE_CODE Your Name\n\n"
        "After you join a company, just send me job requests as plain text."
    )


@router.message()
async def fallback_message(message: Message) -> None:
    await message.answer(
        "🤖 I got your message.\n\n"
        "If you're an owner, try:\n"
        "  /owner_setup My Company Name\n\n"
        "If you're an employee, ask your owner for the office code, then run:\n"
        "  /join_company OFFICE_CODE Your Name"
    )
