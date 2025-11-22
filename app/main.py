from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.routes import health, telegram_webhook
from app.telegram.bot import bot


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await bot.session.close()


app = FastAPI(title="Artlix Backend", lifespan=lifespan)

app.include_router(health.router, prefix="/api")
app.include_router(telegram_webhook.router, prefix="/api")
