from pydantic import BaseModel, Field
from typing import Dict, Optional, List, Union

from ..database.models import db
from ..database.utils import mongo_to_dict

rooms_collection = db.get_collection("rooms")


# Class from db of rooms
class Room(BaseModel):
    name: str = Field(..., description="Room name in RUZ", example="104")


async def get_all() -> List[Dict[str, Union[str, int]]]:
    """ Get all rooms from db """

    return [mongo_to_dict(room) async for room in rooms_collection.find()]


async def get(room_id: str) -> List[Dict[str, Union[str, int]]]:
    """ Get room by its db id """

    room = await rooms_collection.find_one({"_id": room_id})
    if room:
        return mongo_to_dict(room)


async def get_by_name(name: str) -> dict:
    """ Get room by its name """

    room = await rooms_collection.find_one({"name": name})
    if room:
        return mongo_to_dict(room)


async def add(room: dict):
    """ Add room to db """

    room_added = await rooms_collection.insert_one(room)
    new = await rooms_collection.find_one({"_id": room_added.inserted_id})
    return mongo_to_dict(new)


async def add_empty(room_id: str):
    """ Add empty room with specified id to db """

    await rooms_collection.insert_one({"_id": room_id})


async def remove(room_id: str):
    """ Delete room from db """

    await rooms_collection.delete_one({"_id": room_id})


async def patch(room_id: str, new_values: dict):
    """ Patch room """

    await rooms_collection.update_one({"_id": room_id}, {"$set": new_values})


async def put(room_id: str, new_values: dict):
    """ Update room """

    await rooms_collection.update_one(
        {"_id": room_id},
        {"$set": new_values},
    )
