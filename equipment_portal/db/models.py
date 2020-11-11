from pydantic import BaseModel, Field
from bson import ObjectId
from pymongo import MongoClient
from typing import Optional

"""
Для подключения к внешней БД:

client = MongoClient()
db = client['database_url']
"""

DATABASE_NAME, DATABASE_PORT = 'localhost', 27017

#Для подключения к локальной БД:
client = MongoClient("mongodb://host1.miem.vmnet.top:20005")

db = client['equipment']

#Доступ к коллекции
#series_collection = db['equipments']

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


class Equipment(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    ip: str
    name: str
    room_id: int
    audio: str
    merge: str
    port: int
    rtsp: str
    tracking: str
    time_editing: str
    external_id: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }


