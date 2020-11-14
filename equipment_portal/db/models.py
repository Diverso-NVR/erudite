from pydantic import BaseModel, Field
from bson import ObjectId
from pymongo import MongoClient
from typing import Optional


#Класс из бд sources
class Equipment(BaseModel):
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

    #Нужно для того, чтобы _id можно было достать из класса
    class Config:
        fields = {'id': '_id'}

#Класс из бд rooms
class Room(BaseModel):
    id: int
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

    #Нужно для того, чтобы _id можно было достать из класса
    class Config:
        fields = {'id': '_id'}
