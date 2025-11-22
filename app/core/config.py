from functools import lru_cache
from pydantic import AnyUrl
from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    ENV: str = "dev"

    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_WEBHOOK_SECRET_TOKEN: str = "supersecret"

    MONGODB_URI: AnyUrl = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "artlix"

    N8N_BASE_URL: AnyUrl = "http://localhost:5678"
    N8N_WEBHOOK_SECRET: str = "changeme"

    PUBLIC_BASE_URL: str = "https://example.com"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
