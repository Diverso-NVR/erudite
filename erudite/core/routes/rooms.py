from fastapi import APIRouter, Response, status
import logging
from bson.objectid import ObjectId

from ..db.models import (
    Room,
    db,
    mongo_to_dict,
    ErrorResponseModel,
    ResponseModel,
    Response,
    check_ObjectId,
)

router = APIRouter()

logger = logging.getLogger("erudite")

rooms_collection = db.get_collection("rooms")


@router.get(
    "/rooms",
    tags=["rooms"],
    summary="Get all rooms",
    description="Get a list of all rooms in the database",
    response_model=Response,
)
async def list_rooms():
    """Достаем все rooms"""

    return ResponseModel(
        200, [mongo_to_dict(room) async for room in rooms_collection.find()], "Rooms returned successfully"
    )


@router.get(
    "/rooms/{room_id}",
    tags=["rooms"],
    summary="Get a room",
    description="Get a room specified by it's ObjectId",
    response_model=Response,
)
async def find_room(room_id: str):
    """Достаем обьект room из бд"""

    # Проверка на правильность ObjectId
    id = check_ObjectId(room_id)

    if id:
        # Проверка на наличие правилно введенного ObjectId в БД
        room = await rooms_collection.find_one({"_id": id})
        if room:
            logger.info(f"Room {room_id}: {room}")
            return ResponseModel(200, mongo_to_dict(room), "Room returned successfully")
        else:
            message = "This room is not found"
            logger.info(message)
            return ErrorResponseModel(404, message)
    else:
        message = "ObjectId is written in the wrong format"
        return ErrorResponseModel(400, message)


@router.post(
    "/rooms",
    tags=["rooms"],
    summary="Create room",
    description="Create a room specified by it's ObjectId",
    response_model=Response,
)
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
        return ResponseModel(201, mongo_to_dict(new_room), "Room added successfully")


@router.delete(
    "/rooms/{room_id}",
    tags=["rooms"],
    summary="Delete room",
    description="Delete room specified by it's ObjectId",
    response_model=Response,
)
async def delete_room(room_id: str):
    """Удаляем обьект room из бд"""

    # Проверка на правильность ObjectId
    id = check_ObjectId(room_id)

    if id:
        if await rooms_collection.find_one({"_id": id}):
            await rooms_collection.delete_one({"_id": id})
            message = f"Room: {room_id}  -  deleted from the database"
            logger.info(message)
            return ResponseModel(200, message, "Room deleted successfully")
        else:
            message = f"Room: {room_id}  -  not found in the database"
            logger.info(message)
            return ErrorResponseModel(404, message)
    else:
        message = "ObjectId is written in the wrong format"
        return ErrorResponseModel(400, message)


@router.patch(
    "/rooms/{room_id}",
    tags=["rooms"],
    summary="Patch room",
    description="Updates additional atributes of room specified by it's ObjectId",
    response_model=Response,
)
async def patch_room(room_id: str, new_values: dict):
    """Обновляем необязательные поля в room в бд"""

    # Проверка на правильность ObjectId
    id = check_ObjectId(room_id)

    if id:
        if await rooms_collection.find_one({"_id": id}):
            await rooms_collection.update_one({"_id": id}, {"$set": {"additional": new_values}})
            message = f"Room: {room_id}  -  pached"
            logger.info(
                message
            )  # Если ключа нет в обьекте, то будет добавлена новая пара ключ-значение к этому обьекту
            return ResponseModel(200, message, "Room patched successfully")
        else:
            message = f"Room: {room_id}  -  not found in the database"
            logger.info(message)
            return ErrorResponseModel(404, message)
    else:
        message = "ObjectId is written in the wrong format"
        return ErrorResponseModel(400, message)


@router.put(
    "/rooms/{room_id}",
    tags=["rooms"],
    summary="Updates room",
    description="Deletes old atributes of room specified by it's ObjectId and puts in new ones",
    response_model=Response,
)
async def update_room(room_id: str, new_values: Room):
    """Обновляем все поле/поля в room в бд"""

    # Проверка на правильность ObjectId
    id = check_ObjectId(room_id)

    if id:
        if await rooms_collection.find_one({"_id": id}):
            await rooms_collection.delete_one({"_id": id})
            await rooms_collection.insert_one({"_id": id})
            await rooms_collection.update_one(
                {"_id": id}, {"$set": {"name": new_values.name, "additional": mongo_to_dict(new_values.additional)}}
            )
            message = f"Room: {room_id}  -  updated"
            logger.info(
                message
            )  # Если ключа нет в обьекте, то будет добавлена новая пара ключ-значение к этому обьекту
            return ResponseModel(200, message, "Room updated successfully")
        else:
            message = f"Room: {room_id}  -  not found in the database"
            logger.info(message)
            return ErrorResponseModel(404, message)
    else:
        message = "ObjectId is written in the wrong format"
        return ErrorResponseModel(400, message)


@router.get(
    "/rooms/{room_id}/equipment",
    tags=["rooms"],
    summary="Get equipment from the room",
    description="Get a list of equipment from the room specified by it's ObjectId",
    response_model=Response,
)
async def list_room_equipments(room_id: str):
    """Достаем все equipment из конкретной комнаты"""

    # Проверка на правильность ObjectId
    id = check_ObjectId(room_id)

    if id:
        room = await rooms_collection.find_one({"_id": id})
        if room:
            data = [
                mongo_to_dict(equipment) async for equipment in db.equipment.find({"additional": {"room_id": room_id}})
            ]
            return ResponseModel(200, data, "Room updated successfully")
        else:
            message = "This room is not found"
            logger.info(message)
            return ErrorResponseModel(404, message)
    else:
        message = "ObjectId is written in the wrong format"
        return ErrorResponseModel(400, message)
