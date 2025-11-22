from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from app.core.config import get_settings
from app.telegram.handlers import common, owner, employee

settings = get_settings()

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(storage=MemoryStorage())

dp.include_router(common.router)
dp.include_router(owner.router)
dp.include_router(employee.router)
