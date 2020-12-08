from pydantic import BaseModel, Field
from typing import Optional, List, Dict

from ..database.models import db
from ..database.utils import mongo_to_dict


equipment_collection = db.get_collection("equipment")


# Класс из бд sources
class Equipment(BaseModel):
    name: str
    type: str
    additional: Dict[str, str] = Field(...)


async def get_all() -> list:
    """ Достаем оборудование из бд """

    return [mongo_to_dict(equipment) async for equipment in equipment_collection.find()]


async def get(equipment_id: str) -> Equipment:
    """ Достаем оборудование по указанному ObjectId из бд """

    equipment = await equipment_collection.find_one({"_id": equipment_id})
    if equipment:
        return mongo_to_dict(equipment)
    else:
        return False


async def get_by_name(name: str) -> dict:
    """ Достаем оборудование по указанному имени из бд """

    equipment = await equipment_collection.find_one({"name": name})
    if equipment:
        return mongo_to_dict(equipment)
    else:
        return False


async def add(equipment: Equipment) -> dict:
    """ Добавляем оборудование в бд """

    equipment_added = await equipment_collection.insert_one(equipment.dict(by_alias=True))
    new = await equipment_collection.find_one({"_id": equipment_added.inserted_id})
    return mongo_to_dict(new)


async def add_empty(equipment_id: str):
    """ Добавляем оборудование в бд с указанным id """

    await equipment_collection.insert_one({"_id": equipment_id})


async def remove(equipment_id: str):
    """ Удаляем оборудование из бд """

    await equipment_collection.delete_one({"_id": equipment_id})


async def patch_additional(equipment_id: str, new_values: dict):
    """ Патчим дополнительные параметры оборудование """

    await equipment_collection.update_one({"_id": equipment_id}, {"$set": {"additional": new_values}})


async def patch_all(equipment_id: str, new_values: Equipment):
    """ Патчим всю оборудование """

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
    """ Достаем оборудование с указанным room_id из бд """

    return [
        mongo_to_dict(equipment)
        async for equipment in equipment_collection.find({"additional": {"room_id": str(room_id)}})
    ]
