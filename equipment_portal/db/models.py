from pydantic import BaseModel, Field
from bson import ObjectId
from pymongo import MongoClient
from typing import Optional


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

#Класс из бд sources
class Equipment(BaseModel):
    id_: Optional[PyObjectId] = Field(alias='_id')
    id: int
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

#Класс из бд rooms
class Room(BaseModel):
    _id: int
    name: int
    drive: str
    calendar: str
    tracking_state: str
    main_source: str
    screen_source: str
    sound_source: str
    tracking_source: str
    auto_control: str
    stream_url: str
    ruz_id: int

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
