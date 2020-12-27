from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

import logging
from typing import Optional, List

from ..database.models import (
    Message,
)
from ..database import rooms, equipment
from ..database.utils import check_ObjectId

router = APIRouter()

logger = logging.getLogger("erudite")


@router.get(
    "/rooms",
    tags=["rooms"],
    summary="Get all rooms",
    description="Get a list of all rooms in the database or a room by it's ruz_id, if provided",
    response_model=List[rooms.Room],
    responses={404: {"model": Message}},
)
async def list_rooms(
    ruz_id: Optional[int] = None,
):
    if ruz_id is None:
        return await rooms.get_all()

    room = await rooms.get_by_ruz_id(ruz_id)
    if room:
        logger.info(f"Room {ruz_id}: {room}")
        return [room]

    message = "This room is not found"
    logger.info(message)
    return JSONResponse(status_code=404, content={"message": message})


@router.get(
    "/rooms/{room_id}",
    tags=["rooms"],
    summary="Get a room",
    description="Get a room specified by it's ObjectId",
    response_model=rooms.Room,
    responses={400: {"model": Message}, 404: {"model": Message}},
)
async def find_room(room_id: str):
    # Check if ObjectId is in the right format
    id = check_ObjectId(room_id)

    if not id:
        message = "ObjectId is written in the wrong format"
        return JSONResponse(status_code=400, content={"message": message})

    # Check if room with specified ObjectId is in the database
    room = await rooms.get(id)
    if room:
        logger.info(f"Room {room_id}: {room}")
        return room

    message = "This room is not found"
    logger.info(message)
    return JSONResponse(status_code=404, content={"message": message})


@router.post(
    "/rooms",
    tags=["rooms"],
    summary="Create room",
    description="Create a room specified by it's ObjectId",
    response_model=rooms.Room,
    status_code=201,
)
async def create_room(room: rooms.Room, request: Request):
    # Check if room with specified ObjectId is in the database
    if await rooms.get_by_ruz_id(room.ruz_auditorium_oid):
        message = f"Room with ruz_id: '{room.ruz_auditorium_oid}' already exists in the database"
        logger.info(message)
        return JSONResponse(status_code=409, content={"message": message})

    new_room = await rooms.add(await request.json())
    logger.info(
        f"Room with ruz_id: {room.ruz_auditorium_oid}  -  added to the database"
    )
    return new_room


@router.delete(
    "/rooms/{room_id}",
    tags=["rooms"],
    summary="Delete room",
    description="Delete room specified by it's ObjectId",
    response_model=Message,
    responses={400: {"model": Message}, 404: {"model": Message}},
)
async def delete_room(room_id: str):
    # Check if ObjectId is in the right format
    id = check_ObjectId(room_id)

    if not id:
        message = "ObjectId is written in the wrong format"
        return JSONResponse(status_code=400, content={"message": message})

    # Check if room with specified ObjectId is in the database
    if await rooms.get(id):
        await rooms.remove(id)
        message = f"Room: {room_id}  -  deleted from the database"
        logger.info(message)
        return {"message": message}

    message = f"Room: {room_id}  -  not found in the database"
    logger.info(message)
    return JSONResponse(status_code=404, content={"message": message})


@router.patch(
    "/rooms/{room_id}",
    tags=["rooms"],
    summary="Patch room",
    description="Updates additional atributes of room specified by it's ObjectId",
    response_model=Message,
    responses={400: {"model": Message}, 404: {"model": Message}},
)
async def patch_room(room_id: str, new_values: dict):
    # Check if ObjectId is in the right format
    id = check_ObjectId(room_id)

    if not id:
        message = "ObjectId is written in the wrong format"
        return JSONResponse(status_code=400, content={"message": message})

    if not new_values:
        message = "Please fill the request body"
        return JSONResponse(status_code=400, content={"message": message})

    if await rooms.get(id):
        await rooms.patch(id, new_values)
        message = f"Room: {room_id} patched"
        logger.info(message)
        return {"message": message}
    else:
        message = f"Room: {room_id} not found in the database"
        logger.info(message)
        return JSONResponse(status_code=404, content={"message": message})


@router.put(
    "/rooms/{room_id}",
    tags=["rooms"],
    summary="Updates room",
    description="Deletes old atributes of room specified by it's ObjectId and puts in new ones",
    response_model=Message,
    responses={400: {"model": Message}, 404: {"model": Message}},
)
async def update_room(room_id: str, new_values: rooms.Room, request: Request):
    # Check if ObjectId is in the right format
    id = check_ObjectId(room_id)

    if not id:
        message = "ObjectId is written in the wrong format"
        return JSONResponse(status_code=400, content={"message": message})

    if not new_values:
        message = "Please fill the request body"
        return JSONResponse(status_code=400, content={"message": message})

    if await rooms.get(id):
        await rooms.remove(id)
        await rooms.add_empty(id)
        await rooms.put(id, await request.json())
        message = f"Room: {room_id} updated"
        logger.info(message)
        return {"message": message}
    # Check if room with specified ObjectId is in the database
    else:
        message = f"Room: {room_id}  -  not found in the database"
        logger.info(message)
        return JSONResponse(status_code=404, content={"message": message})


@router.get(
    "/rooms/{room_id}/equipment",
    tags=["rooms"],
    summary="Get equipment from the room",
    description="Get a list of equipment from the room specified by it's ObjectId",
    response_model=List[equipment.Equipment],
    responses={400: {"model": Message}, 404: {"model": Message}},
)
async def list_room_equipments(room_id: str):
    # Check if ObjectId is in the right format
    id = check_ObjectId(room_id)

    if not id:
        message = "ObjectId is written in the wrong format"
        return JSONResponse(status_code=400, content={"message": message})

    room = await rooms.get(id)
    if room:
        data = await equipment.sort(id)
        logger.info(data)
        return data
    # Check if equipment with specified room_id is in the database
    else:
        message = "This room is not found"
        logger.info(message)
        return JSONResponse(status_code=404, content={"message": message})
