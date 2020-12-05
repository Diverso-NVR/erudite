from pydantic import BaseModel, Field
from typing import Optional, List
import motor.motor_asyncio
from fastapi.responses import JSONResponse

from ..settings import settings

# Для подключения к внешней БД:
client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongo_url)

# Проверка на тест
TESTING = settings.testing

# Доступ к БД через motor
if TESTING:
    db = client["testDb"]
else:
    db = client[settings.mongo_db_name]


# Класс из бд sources
class Equipment(BaseModel):
    ip: Optional[str] = Field()
    name: Optional[str] = Field()
    room_id: Optional[str] = Field()
    port: Optional[str] = Field()
    rtsp: Optional[str] = Field()


# Класс из бд rooms
class Room(BaseModel):
    name: Optional[str] = Field()


class Discipline(BaseModel):
    course_code: str = Field(...)
    groups: List[str] = Field(...)
    emails: List[str] = Field(...)


def ResponseModel(data, message):
    return JSONResponse(status_code=200, content={"data": data, "message": message})


def ErrorResponseModel(code, message):
    return JSONResponse(status_code=code, content={"message": message})


def mongo_to_dict(obj):
    return {**obj, "_id": str(obj["_id"])}