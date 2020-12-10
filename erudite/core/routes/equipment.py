from fastapi import APIRouter, Request
import logging

from ..database.models import ErrorResponseModel, ResponseModel, Response
from ..database.utils import mongo_to_dict, check_ObjectId
from ..database import equipment

router = APIRouter()

logger = logging.getLogger("erudite")


@router.get(
    "/equipment",
    tags=["equipment"],
    summary="Get equipment",
    description="Get a list of equipment in the database",
    response_model=Response,
)
async def list_equipments():
    return ResponseModel(
        200,
        await equipment.get_all(),
        "Equipment returned successfully",
    )


@router.get(
    "/equipment/{equipment_id}",
    tags=["equipment"],
    summary="Get equipment",
    description="Get an equipment specified by it's ObjectId",
    response_model=Response,
)
async def find_equipment(equipment_id: str):
    # Check if ObjectId is in the right format
    id = check_ObjectId(equipment_id)

    if not id:
        message = "ObjectId is written in the wrong format"
        return ErrorResponseModel(400, message)

    # Check if equipment with specified ObjectId is in the database
    equipment_obj = await equipment.get(id)
    if equipment_obj:
        logger.info(f"Equipment {equipment_id}: {equipment_obj}")
        return ResponseModel(200, mongo_to_dict(equipment_obj), "Equipment returned successfully")
    else:
        message = "This equipment is not found"
        logger.info(message)
        return ErrorResponseModel(404, message)


@router.post(
    "/equipment",
    tags=["equipment"],
    summary="Create equipment",
    description="Create an equipment specified by it's ObjectId",
    response_model=Response,
)
async def create_equipment(val_equipment: equipment.Equipment, request: Request):
    # Check if equipment with specified ObjectId is in the database
    if await equipment.get_by_name(val_equipment.name):
        message = f"Equipment with name: '{val_equipment.name}'  -  already exists in the database"
        logger.info(message)
        return ErrorResponseModel(409, message)

    new_equipment = await equipment.add(await request.json())
    logger.info(f"Equipment: {val_equipment.name}  -  added to the database")

    return ResponseModel(201, new_equipment, "Equipment added successfully")


@router.delete(
    "/equipment/{equipment_id}",
    tags=["equipment"],
    summary="Delete equipment",
    description="Delete an equipment specified by it's ObjectId",
    response_model=Response,
)
async def delete_equipment(equipment_id: str):
    # Check if ObjectId is in the right format
    id = check_ObjectId(equipment_id)

    if not id:
        message = "ObjectId is written in the wrong format"
        return ErrorResponseModel(400, message)

    if await equipment.get(id):
        await equipment.remove(id)
        message = f"Equipment: {equipment_id}  -  deleted from the database"
        logger.info(message)
        return ResponseModel(200, message, "Equipment deleted successfully")
    # Check if equipment with specified ObjectId is in the database
    else:
        message = f"Equipment: {equipment_id}  -  not found in the database"
        logger.info(message)
        return ErrorResponseModel(404, message)


@router.patch(
    "/equipment/{equipment_id}",
    tags=["equipment"],
    summary="Patch equipment",
    description="Updates additional atributes of equipment specified by it's ObjectId",
    response_model=Response,
)
async def patch_equipment(equipment_id: str, new_values: dict) -> str:
    # Check if ObjectId is in the right format
    id = check_ObjectId(equipment_id)

    if not id:
        message = "ObjectId is written in the wrong format"
        return ErrorResponseModel(400, message)

    if await equipment.get(id):
        await equipment.patch_additional(id, new_values)
        message = f"Equipment: {equipment_id}  -  pached"
        logger.info(message)
        return ResponseModel(200, message, "Equipment patched successfully")
    # Check if equipment with specified ObjectId is in the database
    else:
        message = f"Equipment: {equipment_id}  -  not found in the database"
        logger.info(message)
        return ErrorResponseModel(404, message)


@router.put(
    "/equipment/{equipment_id}",
    tags=["equipment"],
    summary="Update equipment",
    description="Deletes old atributes of equipment and puts in new ones",
    response_model=Response,
)
async def update_equipment(equipment_id: str, new_values: equipment.Equipment, request: Request):
    # Check if ObjectId is in the right format
    id = check_ObjectId(equipment_id)

    if not id:
        message = "ObjectId is written in the wrong format"
        return ErrorResponseModel(400, message)

    if await equipment.get(id):
        await equipment.remove(id)
        await equipment.add_empty(id)
        await equipment.patch_all(id, await request.json())
        message = f"Equipment: {equipment_id}  -  updated"
        logger.info(message)
        return ResponseModel(200, message, "Equipment updated successfully")
    # Check if equipment with specified ObjectId is in the database
    else:
        message = f"Equipment: {equipment_id}  -  not found in the database"
        logger.info(message)
        return ErrorResponseModel(404, message)
