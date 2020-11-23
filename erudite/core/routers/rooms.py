from fastapi import APIRouter
import logging
from bson.objectid import ObjectId

<<<<<<< HEAD:erudite/routers/rooms.py
from db.models import Room, db
=======
from ..db.models import Equipment, Room, db
>>>>>>> 6534ed106b1543c69471b7934c3393e0fbb42e52:erudite/core/routers/rooms.py

router = APIRouter()

logger = logging.getLogger("erudite")

rooms_collection = db.get_collection("rooms")


@router.get("/rooms/")
async def list_rooms():
    """Достаем все rooms"""
    rooms_list = []
    async for room in rooms_collection.find():
        rooms_list.append(room)
    if len(rooms_list) == 0:
        logger.info("No rooms found")
        return {}
    else:
        logger.info(f"All rooms in the database: {rooms_list}")
        return rooms_list.__repr__()


@router.get("/rooms/{room_name}")
async def find_room(room_name: str):
    """Достаем обьект room из бд"""

    try:
        room = await rooms_collection.find_one({"_id": ObjectId(room_id)})
        if room:
            logger.info(f"Room {room_id}: {room}")
            return room.__repr__()
        else:
            logger.info("This room is not found")
            return {}
    except Exception:
        logger.error("Wrong ID")
        return "Wrong ID"


@router.post("/rooms/")
async def create_room(room: Room):
    """Добавляем обьект room в бд"""

    if await rooms_collection.find_one({"name": room.name}):
        logger.info(f"Room with name: {room.name}  -  already exists in the database")
        return {}
    else:
        room_added = await rooms_collection.insert_one(room.dict(by_alias=True))
        new_room = await rooms_collection.find_one({"_id": room_added.inserted_id})
        logger.info(f"Room: {room.name}  -  added to the database")

        return {"room": new_room.__repr__()}


@router.delete("/rooms/{room_name}")
async def delete_room(room_name: str):
    """Удаляем обьект room из бд"""

    try:
        if await rooms_collection.find_one({"_id": ObjectId(room_id)}):
            await rooms_collection.delete_one({"_id": ObjectId(room_id)})
            logger.info(f"Room: {room_id}  -  deleted from the database")
            return "done"
        else:
            logger.info(f"Room: {room_id}  -  not found in the database")
            return "Room not found"
    except Exception:
        logger.error("Wrong ID")
        return "Wrong ID"


@router.patch("/rooms/{room_name}")
async def patch_room(room_name: str, new_values_dict: dict):
    """Обновляем/добавляем поле/поля в room в бд"""

    try:
        if await rooms_collection.find_one({"_id": ObjectId(room_id)}):
            await rooms_collection.update_one({"_id": ObjectId(room_id)}, {"$set": new_values})
            logger.info(
                f"Room: {room_id}  -  pached"
            )  # Если ключа нет в обьекте, то будет добавлена новая пара ключ-значение к этому обьекту
            return "done"
        else:
            logger.info(f"Room: {room_id}  -  not found in the database")
            return "Room not found"
    except Exception:
        logger.error("Wrong Id")
        return "Wrong Id"


@router.put("/rooms/{room_name}")
async def update_room(room_name: str, new_values: Room):
    """Обновляем все поле/поля в room в бд"""

    try:
        if await rooms_collection.find_one({"_id": ObjectId(room_id)}):
            await rooms_collection.delete_one({"_id": ObjectId(room_id)})
            await rooms_collection.insert_one({"_id": ObjectId(room_id)})
            await rooms_collection.update_one({"_id": ObjectId(room_id)}, {"$set": new_values})
            logger.info(
                f"Room: {room_id}  -  updated"
            )  # Если ключа нет в обьекте, то будет добавлена новая пара ключ-значение к этому обьекту
            return "done"
        else:
            logger.info(f"Room: {room_id}  -  not found in the database")
            return "Room not found"
    except Exception:
        logger.error("Wrong Id")
        return "Wrong Id"


@router.get("/rooms/{room_name}/equipment")
async def list_room_equipments(room_name: str):
    """Достаем все equipment из конкретной комнаты"""

    equipment_list = []
    async for equipment in db.equipment.find({"room_id": room_id}):
        equipment_list.append(equipment)
    if len(equipment_list) == 0:
        logger.info("No equipment in the room found")
        return {}
    else:
        logger.info(f"Equipment in the room {room_id}: {equipment_list}")
        return equipment_list.__repr__()
