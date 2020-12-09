from pydantic import BaseModel
import motor.motor_asyncio
from fastapi.responses import JSONResponse

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


# Standart class or a json responce
class Response(BaseModel):
    data: list
    message: str


# Respond with a json file
def ResponseModel(code: int, data: str, message: str) -> JSONResponse:
    return JSONResponse(status_code=code, content={"data": data, "message": message})


# Error respond with a json file
def ErrorResponseModel(code: int, message: str) -> JSONResponse:
    return JSONResponse(status_code=code, content={"message": message})
