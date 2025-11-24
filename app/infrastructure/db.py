from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import get_settings

_settings = get_settings()

# Connect to MongoDB using your connection string from settings
client = AsyncIOMotorClient(_settings.MONGODB_URI)

# Use a simple DB name (MongoDB will create it if it doesn't exist)
db_name = getattr(_settings, "MONGODB_DB_NAME", "artlix")
db = client[db_name]

# Collections (tables)
companies_collection = db["companies"]   # owners / companies
employees_collection = db["employees"]   # employees linked to a company
jobs_collection = db["jobs"]             # jobs created by employees
