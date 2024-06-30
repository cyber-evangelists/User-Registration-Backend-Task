# Initializes the db

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from models.models import User

async def init_db_connection():
    client = AsyncIOMotorClient("mongodb://localhost:27017/")
    db_name = "grpc_db"
    await init_beanie(database=client.db_name, document_models=[User])