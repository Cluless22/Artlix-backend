from fastapi import APIRouter, HTTPException
from aiogram.types import Update

from app.telegram.bot import bot, dp

router = APIRouter()


@router.post("/telegram/webhook")
async def telegram_webhook(update: dict):
    """
    Telegram sends all updates here as JSON.
    We turn it into an aiogram Update and feed it to the dispatcher.
    """
    try:
        tg_update = Update.model_validate(update)  # pydantic v2 style
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Telegram update")

    # Let aiogram process handlers: /start, etc.
    await dp.feed_update(bot, tg_update)

    # Telegram doesn't need any message back, just 200 OK/json
    return {"ok": True}
