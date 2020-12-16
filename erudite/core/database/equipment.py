from pydantic import BaseModel
from typing import Dict, Optional, List, Union

from ..database.models import db
from ..database.utils import mongo_to_dict


equipment_collection = db.get_collection("equipment")


# Class from db sources
class Equipment(BaseModel):
    name: str
    type: str


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


async def patch_additional(equipment_id: str, new_values: dict):
    """ Patch equipment """

    await equipment_collection.update_one({"_id": equipment_id}, {"$set": new_values})


async def patch_all(equipment_id: str, new_values: dict):
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
