from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # 🔹 Telegram bot token (from Render env var)
    TELEGRAM_BOT_TOKEN: str

    # 🔹 MongoDB connection string (we keep this as a plain string)
    MONGODB_URI: str

    # 🔹 Database name inside your cluster
    MONGODB_DB_NAME: str = "artlix"

    # 🔹 Public URL of your backend on Render, e.g. "https://artlix.onrender.com"
    WEBHOOK_BASE_URL: str

    # 🔹 Optional: secret token for Telegram webhook security
    WEBHOOK_SECRET_TOKEN: str | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
