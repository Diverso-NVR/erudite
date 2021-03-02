from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from loguru import logger
from typing import Optional, List

from ..database.models import (
    Message,
)
from ..database import rooms, equipment
from ..database.utils import check_ObjectId, get_not_None_args


router = APIRouter()


@router.get(
    "/rooms",
    summary="Get all rooms",
    description=(
        "Get a list of all rooms in the database or a room by any of it's atributes, if provided"
    ),
    response_model=List[rooms.Room],
    responses={404: {"model": Message}},
)
async def list_rooms(
    ruz_type_of_auditorium_oid: Optional[int] = None,
    ruz_amount: Optional[int] = None,
    ruz_auditorium_oid: Optional[int] = None,
    ruz_building: Optional[str] = None,
    ruz_building_gid: Optional[int] = None,
    ruz_number: Optional[str] = None,
    ruz_type_of_auditorium: Optional[str] = None,
):
    if all(
        p is None
        for p in [
            ruz_auditorium_oid,
            ruz_amount,
            ruz_building,
            ruz_building_gid,
            ruz_number,
            ruz_type_of_auditorium,
        ]
    ):
        logger.info("All rooms returned")
        return await rooms.get_all()

    all_args = locals()
    filter_args = get_not_None_args(all_args)

    room_found = await rooms.sort_many(filter_args)
    if room_found:
        logger.info("Room found")
        return room_found

    message = "Rooms are not found"
    logger.info(message)
    return JSONResponse(status_code=404, content={"message": message})


@router.get(
    "/rooms/{room_id}",
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
    summary="Patch room",
    description="Updates additional atributes of room specified by it's ObjectId",
    response_model=Message,
    responses={400: {"model": Message}, 404: {"model": Message}},
)
async def patch_room(room_id: str, new_values: dict, request: Request):
    # Check if ObjectId is in the right format
    id = check_ObjectId(room_id)
    new_values = await request.json()

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
    summary="Updates room",
    description="Deletes old atributes of room specified by it's ObjectId and puts in new ones",
    response_model=Message,
    responses={400: {"model": Message}, 404: {"model": Message}},
)
async def update_room(room_id: str, room: rooms.Room, request: Request):
    # Check if ObjectId is in the right format
    id = check_ObjectId(room_id)
    new_values = await request.json()

    if not id:
        message = "ObjectId is written in the wrong format"
        return JSONResponse(status_code=400, content={"message": message})

    if not new_values:
        message = "Please fill the request body"
        return JSONResponse(status_code=400, content={"message": message})

    if await rooms.get(id):
        await rooms.remove(id)
        await rooms.add_empty(id)
        await rooms.put(id, new_values)
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
