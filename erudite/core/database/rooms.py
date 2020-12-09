from pydantic import BaseModel, Field
from typing import Optional, List, Dict

from ..database.models import db
from ..database.utils import mongo_to_dict

rooms_collection = db.get_collection("rooms")


# Class from db of rooms
class Room(BaseModel):
    name: str
    additional: Dict[str, str] = Field(...)


async def get_all() -> list:
    """ Get all rooms from db """

    return [mongo_to_dict(room) async for room in rooms_collection.find()]


async def get(room_id: str) -> Room:
    """ Get room by its db id """

    room = await rooms_collection.find_one({"_id": room_id})
    if room:
        return mongo_to_dict(room)
    else:
        return False


async def get_by_name(name: str) -> dict:
    """ Get room by its name """

    room = await rooms_collection.find_one({"name": name})
    if room:
        return mongo_to_dict(room)
    else:
        return False


async def add(room: Room) -> dict:
    """ Add room to db """

    room_added = await rooms_collection.insert_one(room.dict(by_alias=True))
    new = await rooms_collection.find_one({"_id": room_added.inserted_id})
    return mongo_to_dict(new)


async def add_empty(room_id: str):
    """ Add empty room with specified id to db """

    await rooms_collection.insert_one({"_id": room_id})


async def remove(room_id: str):
    """ Delete room from db """

    await rooms_collection.delete_one({"_id": room_id})


async def patch_additional(room_id: str, new_values: dict):
    """ Patch room """

    await rooms_collection.update_one({"_id": room_id}, {"$set": {"additional": new_values}})


async def patch_all(room_id: str, new_values: Room):
    """ Patch room """

    await rooms_collection.update_one(
        {"_id": room_id},
        {
            "$set": {
                "name": new_values.name,
                "additional": mongo_to_dict(new_values.additional),
            }
        },
    )
