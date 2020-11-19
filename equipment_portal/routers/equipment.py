from fastapi import APIRouter
import logging
import motor.motor_asyncio

from db.models import Equipment, Room, db

router = APIRouter()

logger = logging.getLogger("equipment_portal")


@router.get("/equipment")
async def list_equipments():
    """Достаем все equipment"""

    equipment_list = []
    async for equipment in db.equipment.find():
        equipment_list.append(Equipment(**equipment))
    try:

        if len(equipment_list) == 0:
            logger.info(f"No items")
            return {}
        else:
            logger.info(f"Equipment in the database: {equipment_list}")
            return {"equipment": equipment_list}
    except:
        logger.info(f"Wrong data in the database")


@router.get("/room_equipment/{room_id}")
async def list_room_equipments(room_id: int):
    """Достаем все equipment из конкретной комнаты"""

    equipment_list = []
    try:
        async for equipment in db.equipment.find({"room_id": room_id}):
            equipment_list.append(Equipment(**equipment))
        if len(equipment_list) == 0:
            logger.info(f"No equipment in the room found")
            return {}
        else:
            logger.info(f"Equipment in the room {room_id}: {equipment_list}")
            return equipment_list
    except:
        logger.info(f"Wrong data in the database")


@router.get("/equipment/{equipment_id}")
async def find_equipment(equipment_id: int):
    """Достаем обьект equipment из бд"""

    try:
        equipment = await db.equipment.find_one({"_id": equipment_id})
        if equipment:
            logger.info(f"Equipment {equipment_id}: {Equipment(**equipment)}")
            return Equipment(**equipment)
        else:
            logger.info(f"This equipment is not found")
            return {}
    except:
        logger.info(f"Wrong data in the database")


@router.post("/equipment")
async def create_equipment(equipment: Equipment):
    """Добавляем обьект equipment в бд"""

    try:
        await db.equipment.insert_one(equipment.dict(by_alias=True))
        logger.info(f"Equipment with id: {equipment.id}  -  added to the database")
    except:
        logger.warning(f"Equipment with id: {equipment.id}  -  already exists in the database")
    return {"equipment": equipment}


@router.delete("/equipment/{equipment_id}")
async def delete_equipment(equipment_id: int):
    """Удаляем обьект equipment из бд"""

    await db.equipment.delete_one({"_id": equipment_id})
    logger.info(f"Equipment with id: {equipment_id}  -  deleted from the database")


@router.put("/equipment/{equipment_id}")
async def update_equipment(equipment_id: int, new_values_dict: dict):
    """Обновляем/добавляем поле/поля в equipment в бд"""

    try:
        await db.equipment.update_one({"_id": equipment_id}, {"$set": new_values_dict})
        logger.info(
            f"Equipment with id: {equipment_id}  -  updated"
        )  # Если ключа нет в обьекте, то будет добавлена новая пара ключ-значение к этому обьекту
    except:
        logger.info(f"Element with this id not found")