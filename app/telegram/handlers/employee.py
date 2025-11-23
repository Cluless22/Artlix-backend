from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ChatType

router = Router()


def _looks_like_company_code(text: str) -> bool:
    """
    Very simple heuristic: our fake company codes look like 'CO-12345'.
    Adjust this later when we have real DB-backed codes.
    """
    text = text.strip()
    if not text.startswith("CO-"):
        return False
    rest = text[3:]
    return rest.isdigit() and 3 <= len(rest) <= 8


@router.message(F.chat.type == ChatType.PRIVATE)
async def handle_employee_private(message: Message) -> None:
    """
    Handle messages from employees in private chat.

    For now:
    - If they send something that looks like a company code -> 'link' them.
    - Otherwise, acknowledge the message as a job / update placeholder.
    """

    text = (message.text or "").strip()

    # Case 1: Looks like a company invite code
    if _looks_like_company_code(text):
        await message.answer(
            "✅ <b>Company code accepted.</b>\n\n"
            "Your chat is now linked to your company (demo mode).\n\n"
            "From now on, you can:\n"
            "• Send job requests (address, time, scope)\n"
            "• Send updates ('job finished', 'delay', etc.)\n\n"
            "Later I’ll automatically:\n"
            "• Update tracking sheets\n"
            "• Ping your owner with summaries\n"
            "• Create calendar events. 📅"
        )
        # In the real version we will:
        # - Look up the company by code in MongoDB
        # - Create/attach an employee record
        # - Store the employee's chat_id for notifications
        return

    # Case 2: Any other text in private from employee -> treat as job/update message
    await message.answer(
        "📝 Got it, I’ve recorded your message.\n\n"
        "In the full version, this will:\n"
        "• Create or update a job entry\n"
        "• Notify your owner\n"
        "• Keep everything in sync.\n\n"
        "For now, you can also try sending your company code if you haven’t yet."
    )
