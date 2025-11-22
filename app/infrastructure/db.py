from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import get_settings

_settings = get_settings()
_client: Optional[AsyncIOMotorClient] = None


def get_mongo_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(str(_settings.MONGODB_URI))
    return _client


def get_db():
    client = get_mongo_client()
    return client[_settings.MONGODB_DB_NAME]


def companies_collection():
    return get_db()["companies"]


def employees_collection():
    return get_db()["employees"]


def jobs_collection():
    return get_db()["jobs"]
