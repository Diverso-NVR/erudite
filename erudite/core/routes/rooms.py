from fastapi import APIRouter, Response, status
import logging
from bson.objectid import ObjectId

from ..db.models import Room, db, mongo_to_dict, ErrorResponseModel, ResponseModel

router = APIRouter()

logger = logging.getLogger("erudite")

rooms_collection = db.get_collection("rooms")


@router.get("/rooms", tags=["rooms"], summary="Get all rooms", description="Get a list of all rooms in the database")
async def list_rooms():
    """Достаем все rooms"""

    return ResponseModel([mongo_to_dict(room) async for room in rooms_collection.find()])


@router.get(
    "/rooms/{room_id}", tags=["rooms"], summary="Get a room", description="Get a room specified by it's ObjectId"
)
async def find_room(room_id: str):
    """Достаем обьект room из бд"""

    # Проверка на правильность ObjectId
    try:
        id = ObjectId(room_id)
    except:
        message = "ObjectId is written in the wrong format"
        logger.info(message)
        return ErrorResponseModel(400, message)

    # Проверка на наличие правилно введенного ObjectId в БД
    room = await rooms_collection.find_one({"_id": id})
    if room:
        logger.info(f"Room {room_id}: {room}")
        return ResponseModel(mongo_to_dict(room))
    else:
        message = "This room is not found"
        logger.info(message)
        return ErrorResponseModel(404, message)


@router.post("/rooms", tags=["rooms"], summary="Create room", description="Create room specified by it's ObjectId")
async def create_room(room: Room):
    """Добавляем обьект room в бд"""

    if await rooms_collection.find_one({"name": room.name}):
        message = f"Room with name: '{room.name}'  -  already exists in the database"
        logger.info(message)
        return ErrorResponseModel(403, message)
    else:
        room_added = await rooms_collection.insert_one(room.dict(by_alias=True))
        new_room = await rooms_collection.find_one({"_id": room_added.inserted_id})
        logger.info(f"Room: {room.name}  -  added to the database")

        return ResponseModel(mongo_to_dict(new_room))


@router.delete(
    "/rooms/{room_id}", tags=["rooms"], summary="Delete room", description="Delete room specified by it's ObjectId"
)
async def delete_room(room_id: str):
    """Удаляем обьект room из бд"""

    # Проверка на правильность ObjectId
    try:
        id = ObjectId(room_id)
    except:
        message = "ObjectId is written in the wrong format"
        logger.info(message)
        return ErrorResponseModel(400, message)

    if await rooms_collection.find_one({"_id": id}):
        await rooms_collection.delete_one({"_id": id})
        logger.info(f"Room: {room_id}  -  deleted from the database")
        return "done"
    else:
        logger.info(f"Room: {room_id}  -  not found in the database")
        return "Room not found"


@router.patch(
    "/rooms/{room_id}",
    tags=["rooms"],
    summary="Patch room",
    description="Changes/adds atributes of room specified by it's ObjectId",
)
async def patch_room(room_id: str, new_values: dict):
    """Обновляем/добавляем поле/поля в room в бд"""

    # Проверка на правильность ObjectId
    try:
        id = ObjectId(room_id)
    except:
        message = "ObjectId is written in the wrong format"
        logger.info(message)
        return ErrorResponseModel(400, message)

    if await rooms_collection.find_one({"_id": id}):
        await rooms_collection.update_one({"_id": id}, {"$set": new_values})
        logger.info(
            f"Room: {room_id}  -  pached"
        )  # Если ключа нет в обьекте, то будет добавлена новая пара ключ-значение к этому обьекту
        return "done"
    else:
        logger.info(f"Room: {room_id}  -  not found in the database")
        return "Room not found"


@router.put(
    "/rooms/{room_id}",
    tags=["rooms"],
    summary="Updates room",
    description="Deletes old atributes of room specified by it's ObjectId and puts in new ones",
)
async def update_room(room_id: str, new_values: Room):
    """Обновляем все поле/поля в room в бд"""

    # Проверка на правильность ObjectId
    try:
        id = ObjectId(room_id)
    except:
        message = "ObjectId is written in the wrong format"
        logger.info(message)
        return ErrorResponseModel(400, message)

    if await rooms_collection.find_one({"_id": id}):
        await rooms_collection.delete_one({"_id": id})
        await rooms_collection.insert_one({"_id": id})
        await rooms_collection.update_one({"_id": id}, {"$set": new_values})
        logger.info(
            f"Room: {room_id}  -  updated"
        )  # Если ключа нет в обьекте, то будет добавлена новая пара ключ-значение к этому обьекту
        return "done"
    else:
        logger.info(f"Room: {room_id}  -  not found in the database")
        return "Room not found"


@router.get(
    "/rooms/{room_id}/equipment",
    tags=["rooms"],
    summary="Get equipment from the room",
    description="Get a list of equipment from the room specified by it's ObjectId",
)
async def list_room_equipments(room_id: str):
    """Достаем все equipment из конкретной комнаты"""

    return [mongo_to_dict(equipment) async for equipment in db.equipment.find({"room_id": room_id})]
