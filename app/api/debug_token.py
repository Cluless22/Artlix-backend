from fastapi import APIRouter
from app.core.config import get_settings

router = APIRouter()

@router.get("/debug/token")
def debug_token():
    settings = get_settings()
    return {"token": settings.TELEGRAM_BOT_TOKEN}
