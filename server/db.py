from beanie import init_beanie
import motor.motor_asyncio
from models import User
import asyncio

mongo_url = 'mongodb://host.docker.internal'


async def init_db():
    """
    Initialize the db function
    """

    try:
        client = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
        client.get_io_loop = asyncio.get_running_loop
        await init_beanie(database=client.db_name, document_models=[User])

        return True
    except Exception as err:

        return False
