from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """
    /start for everyone (owners + employees).
    """
    await message.answer(
        "👋 Hey, I’m <b>Artlix</b>, your construction workflow assistant.\n\n"
        "🏗 <b>Owners</b>\n"
        "• Use /owner_help to see owner commands.\n\n"
        "👷 <b>Employees</b>\n"
        "• If your boss gave you a company code, just send it here to link your chat.\n"
        "• After that, you can send job requests and updates and I’ll keep everything organized."
    )


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    """
    Simple /help command.
    """
    await message.answer(
        "🧠 <b>Artlix help</b>\n\n"
        "Available basics:\n"
        "• /start – intro message\n"
        "• /help – this help\n"
        "• /owner_help – commands for company owners\n\n"
        "Employees can paste their company code to connect their chat."
    )


@router.message()
async def fallback_handler(message: Message) -> None:
    """
    Fallback for any text that isn't caught by other handlers.
    For now just acknowledges the message.
    """
    # For now we just echo. Later we’ll plug in the decision engine + workflows.
    await message.answer(
        "🤖 I got your message.\n"
        "Soon I’ll be able to:\n"
        "• Parse job requests\n"
        "• Update sheets and calendars\n"
        "• Notify your boss automatically.\n\n"
        "For now, try /help."
    )
