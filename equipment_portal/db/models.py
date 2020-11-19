from pydantic import BaseModel, Field
import os
import motor.motor_asyncio

# Достаем uri для доступа к удаленной БД
MONGO_DATABASE_URI = os.environ.get("MONGO_DATABASE_URI")

# Для подключения к внешней БД:
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DATABASE_URI)

# Проверка на тест
TESTING = os.environ.get("TESTING")

# Доступ к БД через motor
if TESTING:
    db = client["testDb"]
else:
    db = client["Equipment"]

# Класс из бд sources
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

    # Нужно для того, чтобы _id можно было достать из класса
    class Config:
        fields = {"id": "_id"}


# Класс из бд rooms
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

    # Нужно для того, чтобы _id можно было достать из класса
    class Config:
        fields = {"id": "_id"}
