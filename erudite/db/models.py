from pydantic import BaseModel
from typing import Optional
import os
import motor.motor_asyncio
from bson import ObjectId


# Для подключения к внешней БД:
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ.get("MONGO_DATABASE_URI"))

# Проверка на тест
TESTING = os.environ.get("TESTING")

# Доступ к БД через motor
if TESTING:
    db = client["testDb"]
else:
    # db = client["erudite"]
    db = client["Equipment"]  # -  Dev


# Класс из бд sources
class Equipment(BaseModel):
    ip: Optional[str] = None
    name: Optional[str] = None
    room_id: Optional[str] = None
    audio: Optional[str] = None
    merge: Optional[str] = None
    port: Optional[int] = None
    rtsp: Optional[str] = None
    tracking: Optional[str] = None
    time_editing: Optional[str] = None
    external_id: Optional[str] = None

    def __repr__(self):
        out = {
            "ip": self.ip,
            "name": self.name,
            "room_id": self.room_id,
            "audio": self.audio,
            "merge": self.merge,
            "port": self.port,
            "rtsp": self.rtsp,
            "tracking": self.tracking,
            "time_editing": self.time_editing,
            "external_id": self.external_id,
        }
        return out


# Класс из бд rooms
class Room(BaseModel):
    name: Optional[str] = None
    drive: Optional[str] = None
    calendar: Optional[str] = None
    tracking_state: Optional[str] = None
    main_source: Optional[str] = None
    screen_source: Optional[str] = None
    sound_source: Optional[str] = None
    tracking_source: Optional[str] = None
    auto_control: Optional[str] = None
    stream_url: Optional[str] = None
    ruz_id: Optional[str] = None

    def __repr__(self):
        out = {
            "name": self.name,
            "drive": self.drive,
            "calendar": self.calendar,
            "tracking_state": self.tracking_state,
            "main_source": self.main_source,
            "screen_source": self.screen_source,
            "sound_source": self.sound_source,
            "tracking_source": self.tracking_source,
            "auto_control": self.auto_control,
            "stream_url": self.stream_url,
            "ruz_id": self.ruz_id,
        }
        return out