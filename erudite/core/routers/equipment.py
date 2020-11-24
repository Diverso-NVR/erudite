from fastapi import APIRouter
import logging
from bson.objectid import ObjectId

from ..db.models import Equipment, db, mongo_to_dict

router = APIRouter()

logger = logging.getLogger("erudite")

equipment_collection = db.get_collection("equipment")


@router.get("/equipment")
async def list_equipments():
    """Достаем все equipment"""

    return [mongo_to_dict(equipment) async for equipment in equipment_collection.find()]


@router.get("/equipment/{equipment_id}")
async def find_equipment(equipment_id: str):
    """Достаем обьект equipment из бд"""

    equipment = await equipment_collection.find_one({"_id": ObjectId(equipment_id)})
    if equipment:
        logger.info(f"Equipment {equipment_id}: {equipment}")
        return mongo_to_dict(equipment)
    else:
        logger.info("This equipment is not found")
        return {}


@router.post("/equipment")
async def create_equipment(equipment: Equipment):
    """Добавляем обьект equipment в бд"""

    equipment_added = await equipment_collection.insert_one(
        equipment.dict(by_alias=True)
    )
    new_equipment = await equipment_collection.find_one(
        {"_id": equipment_added.inserted_id}
    )
    logger.info(f"Equipment: {equipment.name}  -  added to the database")

    return {"equipment": mongo_to_dict(new_equipment)}


@router.delete("/equipment/{equipment_id}")
async def delete_equipment(equipment_id: str):
    """Удаляем обьект equipment из бд"""

    if await equipment_collection.find_one({"_id": ObjectId(equipment_id)}):
        await equipment_collection.delete_one({"_id": ObjectId(equipment_id)})
        logger.info(f"Equipment: {equipment_id}  -  deleted from the database")
        return "done"
    else:
        logger.info(f"Equipment: {equipment_id}  -  not found in the database")
        return "Equipment not found"


@router.patch("/equipment/{equipment_id}")
async def patch_equipment(equipment_id: str, new_values: dict) -> str:
    """Обновляем/добавляем поле/поля в equipment в бд"""

    if await equipment_collection.find_one({"_id": ObjectId(equipment_id)}):
        await equipment_collection.update_one(
            {"_id": ObjectId(equipment_id)}, {"$set": new_values}
        )
        logger.info(
            f"Equipment: {equipment_id}  -  pached"
        )  # Если ключа нет в обьекте, то будет добавлена новая пара ключ-значение к этому обьекту
        return "done"
    else:
        logger.info(f"Equipment: {equipment_id}  -  not found in the database")
        return "Equipment not found"


@router.put("/equipment/{equipment_id}")
async def update_equipment(equipment_id: str, new_values: dict):
    """Обновляем/добавляем поле/поля в equipment в бд"""

    if await equipment_collection.find_one({"_id": ObjectId(equipment_id)}):
        await equipment_collection.delete_one({"_id": ObjectId(equipment_id)})
        await equipment_collection.insert_one({"_id": ObjectId(equipment_id)})
        await equipment_collection.update_one(
            {"_id": ObjectId(equipment_id)}, {"$set": new_values}
        )
        logger.info(
            f"Equipment: {equipment_id}  -  updated"
        )  # Если ключа нет в обьекте, то будет добавлена новая пара ключ-значение к этому обьекту
        return "done"
    else:
        logger.info(f"Equipment: {equipment_id}  -  not found in the database")
        return "Equipment not found"
