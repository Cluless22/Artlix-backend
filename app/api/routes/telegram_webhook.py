from fastapi import APIRouter, HTTPException
from aiogram.types import Update

from app.telegram.bot import bot, dp

router = APIRouter()


@router.post("/telegram/webhook")
async def telegram_webhook(update: dict):
    """
    Telegram sends all updates here as JSON.
    We:
      1) Log the raw update
      2) Let aiogram handlers process it
      3) ALSO send a simple debug reply so we can see something in chat
    """
    print("[telegram_webhook] incoming update:", update)

    # 1) Validate into aiogram Update
    try:
        tg_update = Update.model_validate(update)
    except Exception as e:
        print("[telegram_webhook] bad update:", repr(e))
        raise HTTPException(status_code=400, detail="Invalid Telegram update")

    # 2) Run normal handlers ( /start, /owner_setup, etc. )
    try:
        await dp.feed_update(bot, tg_update)
    except Exception as e:
        print("[telegram_webhook] error while handling update:", repr(e))

    # 3) ALWAYS try to send a simple debug reply back
    try:
        msg = tg_update.message or tg_update.edited_message
        if msg and not msg.from_user.is_bot:
            # Avoid infinite loop: don't reply to our own debug messages
            text = (msg.text or "").strip()
            if "Artlix backend reached. (debug)" not in text:
                await bot.send_message(
                    chat_id=msg.chat.id,
                    text="✅ Artlix backend reached. (debug)",
                )
    except Exception as e:
        print("[telegram_webhook] error sending debug reply:", repr(e))

    return {"ok": True}
