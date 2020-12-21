from pydantic import BaseModel, Field
from typing import Dict, Optional, List, Union

from ..database.models import db
from ..database.utils import mongo_to_dict


equipment_collection = db.get_collection("equipment")


class Equipment(BaseModel):
    name: str = Field(..., description="Name of the equipment", example="Server 1")
    classroom: str = Field(
        None,
        description="Name of the room where equipment is located",
        example="Room 13",
    )
    ip: str = Field(None, description="IP adress of the equipment", example="192.0.2.1")
    type: str = Field(..., description="Type of equipment", example="Server/Jetson")
    login: str = Field(None, description="Login for a camera", example="some_login")
    password: str = Field(
        None, description="Password for a camera", example="some_password"
    )
    port: int = Field(None, description="Port of the equipment", example=8000)
    micro_model: str = Field(
        None, description="Model of a microphone", example="Toshiba"
    )
    rtsp_addres: str = Field(None, description="RTSP adress", example="hz")


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
