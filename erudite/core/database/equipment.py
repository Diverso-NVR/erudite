from pydantic import BaseModel, Field
from typing import Optional, List, Dict

from ..database.models import db
from ..database.utils import mongo_to_dict


equipment_collection = db.get_collection("equipment")


# Class from db sources
class Equipment(BaseModel):
    name: str
    type: str
    additional: Dict[str, str] = Field(...)


async def get_all() -> list:
    """ Get all equipment from db """

    return [mongo_to_dict(equipment) async for equipment in equipment_collection.find()]


async def get(equipment_id: str) -> Equipment:
    """ Get equipment by its db id """

    equipment = await equipment_collection.find_one({"_id": equipment_id})
    if equipment:
        return mongo_to_dict(equipment)
    else:
        return False


async def get_by_name(name: str) -> dict:
    """ Get equipment by its name """

    equipment = await equipment_collection.find_one({"name": name})
    if equipment:
        return mongo_to_dict(equipment)
    else:
        return False


async def add(equipment: Equipment) -> dict:
    """ Add equipment to db """

    equipment_added = await equipment_collection.insert_one(equipment.dict(by_alias=True))
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

    await equipment_collection.update_one({"_id": equipment_id}, {"$set": {"additional": new_values}})


async def patch_all(equipment_id: str, new_values: Equipment):
    """ Patch equipment """

    await equipment_collection.update_one(
        {"_id": equipment_id},
        {
            "$set": {
                "name": new_values.name,
                "type": new_values.type,
                "additional": mongo_to_dict(new_values.additional),
            }
        },
    )


async def sort(room_id: str) -> list:
    """ Get equipment by its db room_id """

    return [
        mongo_to_dict(equipment)
        async for equipment in equipment_collection.find({"additional": {"room_id": str(room_id)}})
    ]
