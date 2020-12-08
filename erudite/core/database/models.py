from pydantic import BaseModel, Field
from typing import List, Dict
import motor.motor_asyncio
from fastapi.responses import JSONResponse

from ..settings import settings


# Для подключения к внешней БД:
client = motor.motor_asyncio.AsyncIOMotorClient(
    settings.mongo_url
)  # "localhost", 27017

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


# Класс дисциплин
class Discipline(BaseModel):
    course_code: str = Field(...)
    groups: List[str] = Field(...)
    emails: List[str] = Field(...)


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
