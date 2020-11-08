from pydantic import BaseModel, Field
from bson import ObjectId
from pymongo import MongoClient
from typing import Optional

"""
Для подключения к внешней БД:

client = MongoClient()
db = client['database_url']
"""

#Для подключения к локальной БД:
client = MongoClient('localhost', 27017)

db = client['NewDB']

#Доступ к коллекции
series_collection = db['series']

#Класс _id
class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class Camera(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    name: str
    login: str
    password: str
    mac: str
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }


