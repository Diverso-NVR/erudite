from fastapi import APIRouter, Request
import logging
from typing import Optional

from ..database.models import (
    ErrorResponseModel,
    ResponseModel,
    Response,
)
from ..database import rooms
from ..database.utils import check_ObjectId
from ..database.equipment import sort

router = APIRouter()

logger = logging.getLogger("erudite")


@router.get(
    "/rooms",
    tags=["rooms"],
    summary="Get all rooms",
    description="Get a list of all rooms in the database or a room by it's ruz_id, if provided",
    response_model=Response,
)
async def list_rooms(
    ruz_id: Optional[int] = None,
):
    if ruz_id is None:
        return ResponseModel(200, await rooms.get_all(), "Rooms returned successfully")

    room = await rooms.get_by_ruz_id(ruz_id)
    if room:
        logger.info(f"Room {ruz_id}: {room}")
        return ResponseModel(200, room, "Room returned successfully")

    message = "This room is not found"
    logger.info(message)
    return ErrorResponseModel(404, message)


@router.get(
    "/rooms/{room_id}",
    tags=["rooms"],
    summary="Get a room",
    description="Get a room specified by it's ObjectId",
    response_model=Response,
)
async def find_room(room_id: str):
    # Check if ObjectId is in the right format
    id = check_ObjectId(room_id)

    if not id:
        message = "ObjectId is written in the wrong format"
        return ErrorResponseModel(400, message)

    # Check if room with specified ObjectId is in the database
    room = await rooms.get(id)
    if room:
        logger.info(f"Room {room_id}: {room}")
        return ResponseModel(200, room, "Room returned successfully")

    message = "This room is not found"
    logger.info(message)
    return ErrorResponseModel(404, message)


@router.post(
    "/rooms",
    tags=["rooms"],
    summary="Create room",
    description="Create a room specified by it's ObjectId",
    response_model=Response,
)
async def create_room(room: rooms.Room, request: Request):
    # Check if room with specified ObjectId is in the database
    if await rooms.get_by_ruz_id(room.ruz_auditorium_oid):
        message = f"Room with ruz_id: '{room.ruz_auditorium_oid}' already exists in the database"
        logger.info(message)
        return ErrorResponseModel(409, message)

    new_room = await rooms.add(await request.json())
    logger.info(
        f"Room with ruz_id: {room.ruz_auditorium_oid}  -  added to the database"
    )
    return ResponseModel(201, new_room, "Room added successfully")


@router.delete(
    "/rooms/{room_id}",
    tags=["rooms"],
    summary="Delete room",
    description="Delete room specified by it's ObjectId",
    response_model=Response,
)
async def delete_room(room_id: str):
    # Check if ObjectId is in the right format
    id = check_ObjectId(room_id)

    if not id:
        message = "ObjectId is written in the wrong format"
        return ErrorResponseModel(400, message)

    # Check if room with specified ObjectId is in the database
    if await rooms.get(id):
        await rooms.remove(id)
        message = f"Room: {room_id}  -  deleted from the database"
        logger.info(message)
        return ResponseModel(200, message, "Room deleted successfully")

    message = f"Room: {room_id}  -  not found in the database"
    logger.info(message)
    return ErrorResponseModel(404, message)


@router.patch(
    "/rooms/{room_id}",
    tags=["rooms"],
    summary="Patch room",
    description="Updates additional atributes of room specified by it's ObjectId",
    response_model=Response,
)
async def patch_room(room_id: str, new_values: dict):
    # Check if ObjectId is in the right format
    id = check_ObjectId(room_id)

    if not id:
        message = "ObjectId is written in the wrong format"
        return ErrorResponseModel(400, message)

    if not new_values:
        message = "Please fill the request body"
        return ErrorResponseModel(400, message)

    if await rooms.get(id):
        await rooms.patch(id, new_values)
        message = f"Room: {room_id}  -  pached"
        logger.info(message)
        return ResponseModel(200, message, "Room patched successfully")
    # Check if room with specified ObjectId is in the database
    else:
        message = f"Room: {room_id}  -  not found in the database"
        logger.info(message)
        return ErrorResponseModel(404, message)


@router.put(
    "/rooms/{room_id}",
    tags=["rooms"],
    summary="Updates room",
    description="Deletes old atributes of room specified by it's ObjectId and puts in new ones",
    response_model=Response,
)
async def update_room(room_id: str, new_values: rooms.Room, request: Request):
    # Check if ObjectId is in the right format
    id = check_ObjectId(room_id)

    if not id:
        message = "ObjectId is written in the wrong format"
        return ErrorResponseModel(400, message)

    if not new_values:
        message = "Please fill the request body"
        return ErrorResponseModel(400, message)

    if await rooms.get(id):
        await rooms.remove(id)
        await rooms.add_empty(id)
        await rooms.put(id, await request.json())
        message = f"Room: {room_id}  -  updated"
        logger.info(message)
        return ResponseModel(200, message, "Room updated successfully")
    # Check if room with specified ObjectId is in the database
    else:
        message = f"Room: {room_id}  -  not found in the database"
        logger.info(message)
        return ErrorResponseModel(404, message)


@router.get(
    "/rooms/{room_id}/equipment",
    tags=["rooms"],
    summary="Get equipment from the room",
    description="Get a list of equipment from the room specified by it's ObjectId",
    response_model=Response,
)
async def list_room_equipments(room_id: str):
    # Check if ObjectId is in the right format
    id = check_ObjectId(room_id)

    if not id:
        message = "ObjectId is written in the wrong format"
        return ErrorResponseModel(400, message)

    room = await rooms.get(id)
    if room:
        data = await sort(id)
        print(data)
        return ResponseModel(200, data, "Room updated successfully")
    # Check if equipment with specified room_id is in the database
    else:
        message = "This room is not found"
        logger.info(message)
        return ErrorResponseModel(404, message)
