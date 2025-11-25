from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from app.core.config import get_settings

settings = get_settings()

# Create bot with correct aiogram v3.13 syntax
bot = Bot(
    token=settings.TELEGRAM_BOT_TOKEN,
    default=DefaultBotProperties(parse_mode="HTML"),
)

# Dispatcher for handlers
dp = Dispatcher()

# Import and register routers from handlers
from app.telegram.handlers import owner, employee, common  # noqa: E402

# Order matters: owner + employee first, then generic common handlers
dp.include_router(owner.router)
dp.include_router(employee.router)
dp.include_router(common.router)
