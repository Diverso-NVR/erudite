from pydantic import BaseModel, Field
from typing import Optional, List, Dict
import motor.motor_asyncio
from fastapi.responses import JSONResponse
from bson.objectid import ObjectId
import logging

from ..settings import settings


# Инициализация логгера
logger = logging.getLogger("erudite")

# Для подключения к внешней БД:
client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongo_url)  # "localhost", 27017

# Проверка на тест
TESTING = settings.testing

# Доступ к БД через motor
if TESTING:
    db = client["testDb"]
else:
    db = client[settings.mongo_db_name]


# Стандртный класс json ответа на запросы
class Response(BaseModel):
    data: list
    message: str


# Функция, возвращающая json файл ответом на запрос
def ResponseModel(code: int, data: str, message: str) -> JSONResponse:
    return JSONResponse(status_code=code, content={"data": data, "message": message})


# Функция, возвращающая json файл с ошибкой в запросе
def ErrorResponseModel(code: int, message: str) -> JSONResponse:
    return JSONResponse(status_code=code, content={"message": message})