from pydantic import BaseModel, Field
from typing import Optional, List, Dict

from ..database.models import db
from ..database.utils import mongo_to_dict

rooms_collection = db.get_collection("rooms")


# Класс из бд rooms
class Room(BaseModel):
    name: str
    additional: Dict[str, str] = Field(...)


async def get_all() -> list:
    """ Достаем комнаты из бд """

    return [mongo_to_dict(room) async for room in rooms_collection.find()]


async def get(room_id: str) -> Room:
    """ Достаем комнату по указанному ObjectId из бд """

    room = await rooms_collection.find_one({"_id": room_id})
    if room:
        return mongo_to_dict(room)
    else:
        return False


async def get_by_name(name: str) -> dict:
    """ Достаем комнату по указанному имени из бд """

    room = await rooms_collection.find_one({"name": name})
    if room:
        return mongo_to_dict(room)
    else:
        return False


async def add(room: Room) -> dict:
    """ Добавляем комнату в бд """

    room_added = await rooms_collection.insert_one(room.dict(by_alias=True))
    new = await rooms_collection.find_one({"_id": room_added.inserted_id})
    return mongo_to_dict(new)


async def add_empty(room_id: str):
    """ Добавляем комнату в бд с указанным id """

    await rooms_collection.insert_one({"_id": room_id})


async def remove(room_id: str):
    """ Удаляем комнату из бд """

    await rooms_collection.delete_one({"_id": room_id})


async def patch_additional(room_id: str, new_values: dict):
    """ Патчим дополнительные параметры комнаты """

    await rooms_collection.update_one({"_id": room_id}, {"$set": {"additional": new_values}})


async def patch_all(room_id: str, new_values: Room):
    """ Патчим всю комнату """

    await rooms_collection.update_one(
        {"_id": room_id}, {"$set": {"name": new_values.name, "additional": mongo_to_dict(new_values.additional)}}
    )
