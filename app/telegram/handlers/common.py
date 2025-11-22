from aiogram import Router, F
from aiogram.types import Message

router = Router()


@router.message(F.text == "/start")
async def cmd_start(message: Message):
    text = (
        "👷‍♂️ Welcome to <b>Artlix</b> – AI workflow assistant for construction.\n\n"
        "• Owners: add me to your team group and send /setup there.\n"
        "• Employees: DM me with /join <office_code> after your boss sets it up."
    )
    await message.answer(text)


@router.message(F.text == "/help")
async def cmd_help(message: Message):
    text = (
        "How to use Artlix:\n\n"
        "1️⃣ Owner adds bot to group and sends /setup.\n"
        "2️⃣ Owner shares office code with employees.\n"
        "3️⃣ Employees DM bot with: /join <office_code>.\n"
        "4️⃣ Employees send natural language job details; I store + notify owner."
    )
    await message.answer(text)


@router.message()
async def fallback(message: Message):
    await message.answer(
        "I didn't recognize that. Use /help to see how to get started."
    )
