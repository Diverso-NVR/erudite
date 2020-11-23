from fastapi import APIRouter
import logging
from bson.objectid import ObjectId

from ..db.models import Equipment, db

router = APIRouter()

logger = logging.getLogger("erudite")

equipment_collection = db.get_collection("equipment")


@router.get("/equipment/")
async def list_equipments():
    """Достаем все equipment"""

    equipment_list = []
    async for equipment in equipment_collection.find():
        equipment_list.append(equipment)
    if len(equipment_list) == 0:
        logger.info("No items")
        return {}
    else:
        logger.info(f"Equipment in the database: {equipment_list}")
        return equipment_list.__repr__()


@router.get("/equipment/{equipment_id}")
async def find_equipment(equipment_id: str):
    """Достаем обьект equipment из бд"""

    try:
        equipment = await equipment_collection.find_one({"_id": ObjectId(equipment_id)})
        if equipment:
            logger.info(f"Equipment {equipment_id}: {equipment}")
            return equipment.__repr__()
        else:
            logger.info("This equipment is not found")
            return {}
    except Exception:
        logger.error("Wrong ID")
        return "Wrong ID"


@router.post("/equipment/")
async def create_equipment(equipment: Equipment):
    """Добавляем обьект equipment в бд"""

    equipment_added = await equipment_collection.insert_one(equipment.dict(by_alias=True))
    new_equipment = await equipment_collection.find_one({"_id": equipment_added.inserted_id})
    logger.info(f"Equipment: {equipment.name}  -  added to the database")

    return {"equipment": new_equipment.__repr__()}


@router.delete("/equipment/{equipment_id}")
async def delete_equipment(equipment_id: str):
    """Удаляем обьект equipment из бд"""

    try:
        if await equipment_collection.find_one({"_id": ObjectId(equipment_id)}):
            await equipment_collection.delete_one({"_id": ObjectId(equipment_id)})
            logger.info(f"Equipment: {equipment_id}  -  deleted from the database")
            return "done"
        else:
            logger.info(f"Equipment: {equipment_id}  -  not found in the database")
            return "Equipment not found"
    except Exception:
        logger.error("Wrong ID")
        return "Wrong ID"


@router.patch("/equipment/{equipment_id}")
async def patch_equipment(equipment_id: str, new_values: dict) -> str:
    """Обновляем/добавляем поле/поля в equipment в бд"""

    try:
        if await equipment_collection.find_one({"_id": ObjectId(equipment_id)}):
            await equipment_collection.update_one({"_id": ObjectId(equipment_id)}, {"$set": new_values})
            logger.info(
                f"Equipment: {equipment_id}  -  pached"
            )  # Если ключа нет в обьекте, то будет добавлена новая пара ключ-значение к этому обьекту
            return "done"
        else:
            logger.info(f"Equipment: {equipment_id}  -  not found in the database")
            return "Equipment not found"
    except Exception:
        logger.error("Wrong Id")
        return "Wrong Id"


@router.put("/equipment/{equipment_id}")
async def update_equipment(equipment_id: str, new_values: dict):
    """Обновляем/добавляем поле/поля в equipment в бд"""

    try:
        if await equipment_collection.find_one({"_id": ObjectId(equipment_id)}):
            await equipment_collection.delete_one({"_id": ObjectId(equipment_id)})
            await equipment_collection.insert_one({"_id": ObjectId(equipment_id)})
            await equipment_collection.update_one({"_id": ObjectId(equipment_id)}, {"$set": new_values})
            logger.info(
                f"Equipment: {equipment_id}  -  updated"
            )  # Если ключа нет в обьекте, то будет добавлена новая пара ключ-значение к этому обьекту
            return "done"
        else:
            logger.info(f"Equipment: {equipment_id}  -  not found in the database")
            return "Equipment not found"
    except Exception:
        logger.error("Wrong Id")
        return "Wrong Id"
