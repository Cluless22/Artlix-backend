from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import get_settings

# ⚙️ Load settings (including MongoDB URI and DB name)
_settings = get_settings()

# ❗ IMPORTANT: cast MONGODB_URI to str so Motor/PyMongo don't choke on a Url object
client = AsyncIOMotorClient(str(_settings.MONGODB_URI))

# Pick the database name from settings
db = client[_settings.MONGODB_DB_NAME]

# Collections we will use
companies_collection = db["companies"]
employees_collection = db["employees"]
jobs_collection = db["jobs"]
