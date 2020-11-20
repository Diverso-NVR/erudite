from fastapi import APIRouter
import logging

from db.models import Equipment, Room, db

router = APIRouter()

logger = logging.getLogger("equipment_portal")


@router.get("/room")
async def list_rooms():
    """Достаем все rooms"""

    rooms_list = []
    try:
        async for room in db.rooms.find():
            rooms_list.append(Room(**room))
        if len(rooms_list) == 0:
            logger.info("No rooms found")
            return {}
        else:
            logger.info(f"All rooms in the database: {rooms_list}")
            return rooms_list
    except Exception:
        logger.error("Wrong data in the database")


@router.get("/room/{room_id}")
async def find_room(room_id: int):
    """Достаем обьект room из бд"""

    try:
        room = await db.rooms.find_one({"_id": room_id})
        if room:
            logger.info(f"Room {room_id}: {Room(**room)}")
            return Room(**room)
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
        logger.info(f"Room with id: {room.id}  -  added to the database")
    except Exception:
        logger.error(f"Room with id: {room.id}  -  already exists in the database")

    return {"room": room}


@router.delete("/room/{room_id}")
async def delete_room(room_id: int):
    """Удаляем обьект room из бд"""

    await db.rooms.delete_one({"_id": room_id})
    logger.info(f"Room with id: {room_id}  -  deleted from the database")


@router.put("/room/{room_id}")
async def update_room(room_id: int, new_values_dict: dict):
    """Обновляем/добавляем поле/поля в room в бд"""

    try:
        await db.rooms.update_one({"_id": room_id}, {"$set": new_values_dict})
        logger.info(
            f"Room with id: {room_id}  -  updated"
        )  # Если ключа нет в обьекте, то будет добавлена новая пара ключ-значение к этому обьекту
    except Exception:
        logger.error("Element with this id not found")


@router.get("/room/{room_id}/equipment")
async def list_room_equipments(room_id: int):
    """Достаем все equipment из конкретной комнаты"""

    equipment_list = []
    try:
        async for equipment in db.equipment.find({"room_id": room_id}):
            equipment_list.append(Equipment(**equipment))
        if len(equipment_list) == 0:
            logger.info("No equipment in the room found")
            return {}
        else:
            logger.info(f"Equipment in the room {room_id}: {equipment_list}")
            return equipment_list
    except Exception:
        logger.error("Wrong data in the database")
