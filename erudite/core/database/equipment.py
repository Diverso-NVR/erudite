from pydantic import BaseModel, Field
from typing import Dict, Optional, List, Union

from ..database.models import db
from ..database.utils import mongo_to_dict


equipment_collection = db.get_collection("equipment")


class Equipment(BaseModel):
    id: str = Field(...)

    name: str = Field(
        ..., description="Name of the equipment", example="Камера 306 на доску"
    )
    type: str = Field(..., description="Type of equipment", example="ONVIF-camera")

    room_name: str = Field(
        None,
        description="Room name where equipment is located",
        example="306",
    )
    room_id: str = Field(
        None,
        description="Room id in erudite, it provides mto relationship to room",
    )

    ip: str = Field(
        None, description="IP adress of the equipment", example="172.18.191.62"
    )
    port: int = Field(None, description="Port of the equipment", example=80)
    rtsp_main: str = Field(
        None,
        description="RTSP main address",
        example="rtsp://172.18.191.62:554/Streaming/Channels/1",
    )


async def get_all() -> List[Dict[str, Union[str, int]]]:
    """ Get all equipment from db """

    return [mongo_to_dict(equipment) async for equipment in equipment_collection.find()]


async def get(equipment_id: str) -> Optional[Dict[str, Union[str, int]]]:
    """ Get equipment by its db id """

    equipment = await equipment_collection.find_one({"_id": equipment_id})
    if equipment:
        return mongo_to_dict(equipment)


async def get_by_name(name: str) -> Optional[Dict[str, Union[str, int]]]:
    """ Get equipment by its name """

    equipment = await equipment_collection.find_one({"name": name})
    if equipment:
        return mongo_to_dict(equipment)


async def add(equipment: dict) -> Optional[Dict[str, Union[str, int]]]:
    """ Add equipment to db """

    equipment_added = await equipment_collection.insert_one(equipment)
    new = await equipment_collection.find_one({"_id": equipment_added.inserted_id})
    return mongo_to_dict(new)


async def add_empty(equipment_id: str):
    """ Add empty equipment with specified id to db """

    await equipment_collection.insert_one({"_id": equipment_id})


async def remove(equipment_id: str):
    """ Delete equipment from db """

    await equipment_collection.delete_one({"_id": equipment_id})


async def patch(equipment_id: str, new_values: dict):
    """ Patch equipment """

    await equipment_collection.update_one(
        {"_id": equipment_id},
        {"$set": new_values},
    )


async def sort(room_id: str) -> list:
    """ Get equipment by its db room_id """

    return [
        mongo_to_dict(equipment)
        async for equipment in equipment_collection.find({"room_id": str(room_id)})
    ]


async def sort_many(attributes: dict) -> list:
    """ Get equipment by its db attributes """

    return [
        mongo_to_dict(equipment)
        async for equipment in equipment_collection.find(attributes)
    ]
