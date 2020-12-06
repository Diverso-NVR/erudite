from pydantic import BaseModel, Field
from typing import Optional, List, Dict
import motor.motor_asyncio
from fastapi.responses import JSONResponse
from bson.objectid import ObjectId
import logging

from ..settings import settings

logger = logging.getLogger("erudite")

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


def ResponseModel(code: int, data: str, message: str) -> JSONResponse:
    return JSONResponse(status_code=code, content={"data": data, "message": message})


def ErrorResponseModel(code: int, message: str) -> JSONResponse:
    return JSONResponse(status_code=code, content={"message": message})


# Перевод модели в словарь
def mongo_to_dict(obj):
    id = obj.get("_id")
    if id:
        return {**obj, "_id": str(obj["_id"])}
    else:
        return {**obj}


# Проверка на правильность формата введенного ObjectId
def check_ObjectId(id: str) -> str:
    try:
        new_id = ObjectId(id)
        return new_id
    except:
        message = "ObjectId is written in the wrong format"
        logger.info(message)
        return False