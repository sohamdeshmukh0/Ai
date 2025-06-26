from motor.motor_asyncio import AsyncIOMotorClient
from .config import Config

client = AsyncIOMotorClient(Config.MONGO_URI)
db = client.get_database()  # Use default database in URI
users_collection = db.users
questions_collection = db.questionnaire
projects_collection = db.project