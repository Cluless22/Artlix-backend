from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from app.core.config import get_settings

settings = get_settings()

bot = Bot(
    token=settings.TELEGRAM_BOT_TOKEN,
    default=DefaultBotProperties(parse_mode="HTML"),
)

dp = Dispatcher()

from app.telegram.handlers import owner, employee, common  # noqa: E402

# Order: specific logic first, generic fallback last
dp.include_router(owner.router)
dp.include_router(employee.router)
dp.include_router(common.router)
