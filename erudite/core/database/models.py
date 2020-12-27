from pydantic import BaseModel
import motor.motor_asyncio

from ..settings import settings


# Connection to a remote db:
client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongo_url)

# Check if it's a test run
TESTING = settings.testing

# Access to a db using motor
if TESTING:
    db = client["testDb"]
else:
    db = client[settings.mongo_db_name]


class Message(BaseModel):
    message: str
