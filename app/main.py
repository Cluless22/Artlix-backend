from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.routes import health, telegram_webhook
from app.telegram.bot import bot


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic (optional)
    yield
    # Shutdown logic
    await bot.session.close()


app = FastAPI(title="Artlix Backend", lifespan=lifespan)

# Include API routes
app.include_router(health.router, prefix="/api")
app.include_router(telegram_webhook.router, prefix="/api")
