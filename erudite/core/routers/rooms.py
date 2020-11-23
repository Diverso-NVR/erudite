from fastapi import APIRouter
import logging

from ..db.models import Equipment, Room, db

router = APIRouter()

logger = logging.getLogger("erudite")


@router.get("/room")
async def list_rooms():
    """Достаем все rooms"""
    rooms_list = []
    # try:

    async for room in db.rooms.find():
        name = room.get("_id")
        rooms_list.append(room)
    if len(rooms_list) == 0:
        logger.info("No rooms found")
        return {}
    else:
        logger.info(f"All rooms in the database: {rooms_list}")
        return rooms_list.__repr__()
    # except Exception:
    # logger.error("Wrong data in the database")


@router.get("/room/{room_name}")
async def find_room(room_name: str):
    """Достаем обьект room из бд"""

    try:
        room = await db.rooms.find_one({"_id": room_name})
        if room:
            logger.info(f"Room {room_name}: {Room(**room)}")
            return Room(**room).__repr__()
        else:
            logger.info("This room is not found")
            return {}
    except Exception:
        logger.error("Wrong data in the database")


@router.post("/room")
async def create_room(room: Room):
    """Добавляем обьект room в бд"""

    try:
        await db.rooms.insert_one(room.dict(by_alias=True))
        logger.info(f"Room: {room.name}  -  added to the database")
    except Exception:
        logger.error(f"Room: {room.name}  -  already exists in the database")

    return {"room": room}


@router.delete("/room/{room_name}")
async def delete_room(room_name: str):
    """Удаляем обьект room из бд"""

    await db.rooms.delete_one({"_id": room_name})
    logger.info(f"Room: {room_name}  -  deleted from the database")


@router.patch("/room/{room_name}")
async def patch_room(room_name: str, new_values_dict: dict):
    """Обновляем/добавляем поле/поля в room в бд"""

    try:
        await db.rooms.update_one({"_id": room_name}, {"$set": new_values_dict})
        logger.info(
            f"Room: {room_name}  -  pached"
        )  # Если ключа нет в обьекте, то будет добавлена новая пара ключ-значение к этому обьекту
    except Exception:
        logger.error("Element with this name not found")


@router.put("/room/{room_name}")
async def update_room(room_name: str, new_values: Room):
    """Обновляем все поле/поля в room в бд"""

    # try:
    await db.rooms.delete_one({"_id": room_name})
    await db.rooms.insert_one(new_values.dict(by_alias=True))
    logger.info(
        f"Room: {room_name}  -  updated"
    )  # Если ключа нет в обьекте, то будет добавлена новая пара ключ-значение к этому обьекту
    # except Exception:
    # logger.error("Element with this name not found")


@router.get("/room/{room_name}/equipment")
async def list_room_equipments(room_name: str):
    """Достаем все equipment из конкретной комнаты"""

    equipment_list = []
    try:
        async for equipment in db.equipment.find({"room_name": room_name}):
            equipment_list.append(Equipment(**equipment))
        if len(equipment_list) == 0:
            logger.info("No equipment in the room found")
            return {}
        else:
            logger.info(f"Equipment in the room {room_name}: {equipment_list}")
            return equipment_list
    except Exception:
        logger.error("Wrong data in the database")
