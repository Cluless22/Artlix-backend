from fastapi import APIRouter, Request, Header, HTTPException
from aiogram.types import Update

from app.core.config import get_settings
from app.telegram.bot import bot, dp

router = APIRouter()
settings = get_settings()


@router.post("/telegram/webhook")
async def telegram_webhook(
    request: Request,
    x_telegram_bot_api_secret_token: str | None = Header(default=None),
):
    expected = settings.TELEGRAM_WEBHOOK_SECRET_TOKEN
    if expected and x_telegram_bot_api_secret_token != expected:
        raise HTTPException(status_code=403, detail="Invalid secret token")

    data = await request.json()
    update = Update.model_validate(data)

    await dp.feed_update(bot=bot, update=update)
    return {"ok": True}
