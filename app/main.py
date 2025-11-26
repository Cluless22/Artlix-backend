from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.telegram_webhook import router as telegram_router
from app.api.debug_token import router as debug_router

app = FastAPI()

app.include_router(health_router)
app.include_router(telegram_router)
app.include_router(debug_router)
