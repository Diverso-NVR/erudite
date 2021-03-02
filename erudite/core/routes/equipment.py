from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from loguru import logger
from typing import Optional, List

from ..database.models import Message
from ..database.utils import check_ObjectId, get_not_None_args
from ..database import equipment

router = APIRouter()


@router.get(
    "/equipment",
    summary="Get equipment",
    description=(
        "Get a list of equipment in the database or an equipment by any of it's atributes, if provided"
    ),
    response_model=List[equipment.Equipment],
    responses={404: {"model": Message}},
)
async def list_equipments(
    name: Optional[str] = None,
    type: Optional[str] = None,
    room_name: Optional[str] = None,
    room_id: Optional[str] = None,
    ip: Optional[str] = None,
    port: Optional[int] = None,
    rtsp_main: Optional[str] = None,
):
    if (
        name is None
        and type is None
        and room_name is None
        and room_id is None
        and ip is None
        and port is None
        and rtsp_main is None
    ):
        return await equipment.get_all()

    all_args = locals()
    filter_args = get_not_None_args(all_args)

    equipment_found = await equipment.sort_many(filter_args)
    if equipment_found:
        logger.info("Equipment found")
        return equipment_found

    message = "Equipment are not found"
    logger.info(message)
    return JSONResponse(status_code=404, content={"message": message})


@router.get(
    "/equipment/{equipment_id}",
    summary="Get equipment",
    description="Get an equipment specified by it's ObjectId",
    response_model=equipment.Equipment,
    responses={404: {"model": Message}},
)
async def find_equipment(equipment_id: str):
    # Check if ObjectId is in the right format
    id = check_ObjectId(equipment_id)

    if not id:
        return JSONResponse(
            status_code=404,
            content={"message": "ObjectId is written in the wrong format"},
        )

    # Check if equipment with specified ObjectId is in the database
    equipment_obj = await equipment.get(id)
    if equipment_obj:
        logger.info(f"Equipment {equipment_id}: {equipment_obj}")
        return equipment_obj
    else:
        message = "This equipment is not found"
        logger.info(message)

        return JSONResponse(status_code=404, content={"message": message})


@router.post(
    "/equipment",
    summary="Create equipment",
    description="Create an equipment specified by it's ObjectId",
    response_model=equipment.Equipment,
    status_code=201,
    responses={409: {"model": Message}},
)
async def create_equipment(val_equipment: equipment.Equipment, request: Request):
    # Check if equipment with specified ObjectId is in the database
    if await equipment.get_by_name(val_equipment.name):
        message = f"Equipment with name: '{val_equipment.name}'  -  already exists in the database"
        logger.info(message)
        return JSONResponse(status_code=409, content={"message": message})

    new_equipment = await equipment.add(await request.json())
    logger.info(f"Equipment: {val_equipment.name}  -  added to the database")

    return new_equipment


@router.delete(
    "/equipment/{equipment_id}",
    summary="Delete equipment",
    description="Delete an equipment specified by it's ObjectId",
    response_model=Message,
    responses={400: {"model": Message}, 404: {"model": Message}},
)
async def delete_equipment(equipment_id: str):
    # Check if ObjectId is in the right format
    id = check_ObjectId(equipment_id)

    if not id:
        message = "ObjectId is written in the wrong format"
        return JSONResponse(status_code=400, content={"message": message})

    if await equipment.get(id):
        await equipment.remove(id)
        message = f"Equipment: {equipment_id} deleted from the database"
        logger.info(message)
        return {"message": message}
    else:
        message = f"Equipment: {equipment_id} not found in the database"
        logger.info(message)
        return JSONResponse(status_code=404, content={"message": message})


@router.patch(
    "/equipment/{equipment_id}",
    summary="Patch equipment",
    description="Updates additional atributes of equipment specified by it's ObjectId",
    response_model=Message,
    responses={400: {"model": Message}, 404: {"model": Message}},
)
async def patch_equipment(equipment_id: str, request: Request) -> str:
    # Check if ObjectId is in the right format
    id = check_ObjectId(equipment_id)

    if not id:
        message = "ObjectId is written in the wrong format"
        return JSONResponse(status_code=400, content={"message": message})

    if await equipment.get(id):
        await equipment.patch(id, await request.json())
        message = f"Equipment {equipment_id} patched"
        logger.info(message)
        return {"message": message}
    else:
        message = f"Equipment: {equipment_id}  -  not found in the database"
        logger.info(message)
        return JSONResponse(status_code=404, content={"message": message})


@router.put(
    "/equipment/{equipment_id}",
    summary="Update equipment",
    description="Deletes old atributes of equipment and puts in new ones",
    response_model=Message,
    responses={400: {"model": Message}, 404: {"model": Message}},
)
async def update_equipment(
    equipment_id: str, equipment: equipment.Equipment, request: Request
):
    # Check if ObjectId is in the right format
    id = check_ObjectId(equipment_id)

    if not id:
        message = "ObjectId is written in the wrong format"
        return JSONResponse(status_code=400, content={"message": message})

    if await equipment.get(id):
        await equipment.remove(id)
        await equipment.add_empty(id)
        await equipment.patch(id, await request.json())
        message = f"Equipment {equipment_id} updated"
        logger.info(message)
        return {"message": message}
    else:
        message = f"Equipment {equipment_id} not found in the database"
        logger.info(message)
        return JSONResponse(status_code=404, content={"message": message})
