from pydantic import BaseModel, Field
from typing import Optional, List, Dict
import motor.motor_asyncio
from fastapi.responses import JSONResponse

from ..settings import settings

# Для подключения к внешней БД:
client = motor.motor_asyncio.AsyncIOMotorClient("localhost", 27017)  # settings.mongo_url)

# Проверка на тест
TESTING = settings.testing

# Доступ к БД через motor
if TESTING:
    db = client["testDb"]
else:
    db = client[settings.mongo_db_name]


# Класс из бд sources
class Equipment(BaseModel):
    name: str
    type: str
    additional: Dict[str, str] = Field(...)


# Класс из бд rooms
class Room(BaseModel):
    name: str
    additional: Dict[str, str] = Field(...)


class Discipline(BaseModel):
    course_code: str = Field(...)
    groups: List[str] = Field(...)
    emails: List[str] = Field(...)


class Response(BaseModel):
    data: list
    message: str


def ResponseModel(code, data, message):
    return JSONResponse(status_code=code, content={"data": data, "message": message})


def ErrorResponseModel(code, message):
    return JSONResponse(status_code=code, content={"message": message})


def mongo_to_dict(obj):
    return {**obj, "_id": str(obj["_id"])}


def mongo_to_dict_no_id(obj):
    return {**obj}