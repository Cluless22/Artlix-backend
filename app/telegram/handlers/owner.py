from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ChatType

router = Router()


def _fake_company_code_for_now(user_id: int) -> str:
    """
    Temporary helper to simulate generating a company code.
    Later we will replace this with a real DB call.
    """
    # Very simple deterministic code for demo purposes
    return f"CO-{user_id % 100000:05d}"


@router.message(Command("owner_help"))
async def owner_help(message: Message) -> None:
    """
    Show help for owners.
    Only makes sense in private chat with the owner.
    """
    if message.chat.type != ChatType.PRIVATE:
        await message.answer("ℹ️ Owner commands should be used in a private chat with the bot.")
        return

    await message.answer(
        "🏗 <b>Owner control panel</b>\n\n"
        "Right now basic owner commands are:\n"
        "• /owner_code – get your company invite code to give to employees\n\n"
        "Employees will DM this bot, send that code, and I’ll link their chat "
        "to your company. Later, I’ll:\n"
        "• Track job intake\n"
        "• Sync with Google Sheets + Calendar\n"
        "• Send you daily digests and alerts. 🔔"
    )


@router.message(Command("owner_code"))
async def owner_code(message: Message) -> None:
    """
    Return a simple 'company code' for the owner to share with employees.
    Later this will be backed by MongoDB.
    """
    if message.chat.type != ChatType.PRIVATE:
        await message.answer("ℹ️ Please DM me this command in private to get your company code.")
        return

    owner_id = message.from_user.id
    code = _fake_company_code_for_now(owner_id)

    await message.answer(
        "🔐 <b>Your Artlix company code</b>\n\n"
        f"<code>{code}</code>\n\n"
        "👉 Share this code with your employees.\n"
        "They should:\n"
        "1️⃣ Open a private chat with this bot\n"
        "2️⃣ Paste this code\n"
        "3️⃣ Then they get their own AI-powered workspace."
    )
