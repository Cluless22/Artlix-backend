from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """
    Handles the /start command for any user.
    """
    await message.answer(
        "👋 Hey! I'm Artlix.\n\n"
        "I help construction teams capture jobs, schedule work,\n"
        "and keep owners in the loop.\n\n"
        "🧱 If you're an *owner*, use /owner_setup to create your company space.\n"
        "👷 If you're an *employee*, your boss will share a code so you can connect."
    )


@router.message()
async def fallback_message(message: Message) -> None:
    """
    Handles any message that didn't match other handlers.
    For now it's just a simple reply, later we'll connect this to the decision engine.
    """
    await message.answer(
        "🤖 I got your message!\n"
        "Soon I'll be smart enough to:\n"
        "• Parse job requests\n"
        "• Log them to Sheets\n"
        "• Notify your team\n\n"
        "For now, try /start or /owner_setup."
    )
