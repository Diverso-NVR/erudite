from fastapi import APIRouter, Response, status
import logging
from bson.objectid import ObjectId

from ..db.models import Room, db, mongo_to_dict

router = APIRouter()

logger = logging.getLogger("erudite")

rooms_collection = db.get_collection("rooms")


@router.get("/rooms", tags=["rooms"])
async def list_rooms():
    """Достаем все rooms"""

    return [mongo_to_dict(room) async for room in rooms_collection.find()]


@router.get("/rooms/{room_id}", tags=["rooms"], response_model=Room)
async def find_room(room_id: str):
    """Достаем обьект room из бд"""

    room = await rooms_collection.find_one({"_id": ObjectId(room_id)})
    if room:
        logger.info(f"Room {room_id}: {room}")
        return mongo_to_dict(room)
    else:
        logger.info("This room is not found")
        return {}


@router.post("/rooms", tags=["rooms"], response_model=Room)
async def create_room(room: Room):
    """Добавляем обьект room в бд"""

    if await rooms_collection.find_one({"name": room.name}):
        logger.info(f"Room with name: {room.name}  -  already exists in the database")
        return {}
    else:
        room_added = await rooms_collection.insert_one(room.dict(by_alias=True))
        new_room = await rooms_collection.find_one({"_id": room_added.inserted_id})
        logger.info(f"Room: {room.name}  -  added to the database")

        return {"message": mongo_to_dict(new_room)}


@router.delete("/rooms/{room_id}", tags=["rooms"])
async def delete_room(room_id: str):
    """Удаляем обьект room из бд"""

    if await rooms_collection.find_one({"_id": ObjectId(room_id)}):
        await rooms_collection.delete_one({"_id": ObjectId(room_id)})
        logger.info(f"Room: {room_id}  -  deleted from the database")
        return "done"
    else:
        logger.info(f"Room: {room_id}  -  not found in the database")
        return "Room not found"


@router.patch("/rooms/{room_id}", tags=["rooms"])
async def patch_room(room_id: str, new_values: dict):
    """Обновляем/добавляем поле/поля в room в бд"""

    if await rooms_collection.find_one({"_id": ObjectId(room_id)}):
        await rooms_collection.update_one({"_id": ObjectId(room_id)}, {"$set": new_values})
        logger.info(
            f"Room: {room_id}  -  pached"
        )  # Если ключа нет в обьекте, то будет добавлена новая пара ключ-значение к этому обьекту
        return "done"
    else:
        logger.info(f"Room: {room_id}  -  not found in the database")
        return "Room not found"


@router.put("/rooms/{room_id}", tags=["rooms"])
async def update_room(room_id: str, new_values: Room):
    """Обновляем все поле/поля в room в бд"""

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


@router.get("/rooms/{room_id}/equipment", tags=["rooms"])
async def list_room_equipments(room_id: str):
    """Достаем все equipment из конкретной комнаты"""

    return [mongo_to_dict(equipment) async for equipment in db.equipment.find({"room_id": room_id})]
