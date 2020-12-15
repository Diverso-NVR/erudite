from pydantic import BaseModel, Field
from typing import Dict, List, Union
from bson.objectid import ObjectId

from ..database.models import db
from ..database.utils import mongo_to_dict


rooms_collection = db.get_collection("rooms")


class Room(BaseModel):
    ruz_type_of_auditorium_oid: int = Field(..., description="Room type in RUZ", example=1019)
    ruz_amount: int = Field(..., description="HZ", example=1000)
    ruz_auditorium_oid: int = Field(..., description="Room id in RUZ", example=3308)
    ruz_building: str = Field(
        ...,
        description="Building in which room is located",
        example="Таллинская ул., д, 34",
    )
    ruz_building_gid: int = Field(
        ..., description="Building id in which room is located", example=92
    )
    ruz_number: str = Field(..., description="HZ", example="on-line консультация 9")
    ruz_type_of_auditorium: str = Field(..., description="Type of room", example="Семинарская")


async def get_all() -> List[Dict[str, Union[str, int]]]:
    """ Get all rooms from db """

    return [mongo_to_dict(room) async for room in rooms_collection.find()]


async def get(room_id: ObjectId) -> List[Dict[str, Union[str, int]]]:
    """ Get room by its db id """

    room = await rooms_collection.find_one({"_id": room_id})
    if room:
        return mongo_to_dict(room)


async def get_by_ruz_id(ruz_auditorium_oid: int) -> dict:
    """ Get room by its ruz_auditorium_oid """

    room = await rooms_collection.find_one({"ruz_auditorium_oid": ruz_auditorium_oid})
    if room:
        return mongo_to_dict(room)


async def add(room: dict):
    """ Add room to db """

    room_added = await rooms_collection.insert_one(room)
    new = await rooms_collection.find_one({"_id": room_added.inserted_id})
    return mongo_to_dict(new)


async def add_empty(room_id: ObjectId):
    """ Add empty room with specified id to db """

    await rooms_collection.insert_one({"_id": room_id})


async def remove(room_id: ObjectId):
    """ Delete room from db """

    await rooms_collection.delete_one({"_id": room_id})


async def patch(room_id: ObjectId, new_values: dict):
    """ Patch room """

    await rooms_collection.update_one({"_id": room_id}, {"$set": new_values})


async def put(room_id: ObjectId, new_values: dict):
    """ Update room """

    await rooms_collection.update_one(
        {"_id": room_id},
        {"$set": new_values},
    )
