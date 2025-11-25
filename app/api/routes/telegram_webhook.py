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
        tg_update = Update.model_validate(update)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Telegram update")

    try:
        await dp.feed_update(bot, tg_update)
    except Exception as e:
        # Log the error and avoid crashing the webhook (no 500 to Telegram)
        print("[telegram_webhook] error while handling update:", repr(e))
        # Still return 200 so Telegram doesn't keep retrying this update
        return {"ok": False}

    return {"ok": True}
