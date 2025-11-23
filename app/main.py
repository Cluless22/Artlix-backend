from fastapi import FastAPI

from app.api.routes import health, telegram_webhook

app = FastAPI()


# Include simple health check
app.include_router(health.router)

# Include Telegram webhook endpoint
app.include_router(telegram_webhook.router)
