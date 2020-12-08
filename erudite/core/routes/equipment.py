from fastapi import APIRouter
import logging
from bson.objectid import ObjectId

from ..database.models import ErrorResponseModel, ResponseModel, Response
from ..database.utils import mongo_to_dict, check_ObjectId
from ..database.equipment import (
    get_all,
    get,
    get_by_name,
    add,
    remove,
    add_empty,
    patch_additional,
    patch_all,
    Equipment,
)

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
    """Достаем все equipment"""

    return ResponseModel(
        200,
        await get_all(),
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
    """Достаем обьект equipment из бд"""

    # Проверка на правильность ObjectId
    id = check_ObjectId(equipment_id)

    if id:
        # Проверка на наличие правилно введенного ObjectId в БД
        equipment = await get(id)
        if equipment:
            logger.info(f"Equipment {equipment_id}: {equipment}")
            return ResponseModel(200, mongo_to_dict(equipment), "Equipment returned successfully")
        else:
            message = "This equipment is not found"
            logger.info(message)
            return ErrorResponseModel(404, message)
    else:
        message = "ObjectId is written in the wrong format"
        return ErrorResponseModel(400, message)


@router.post(
    "/equipment",
    tags=["equipment"],
    summary="Create equipment",
    description="Create an equipment specified by it's ObjectId",
    response_model=Response,
)
async def create_equipment(equipment: Equipment):
    """Добавляем обьект equipment в бд"""

    if await get_by_name(equipment.name):
        message = f"Equipment with name: '{equipment.name}'  -  already exists in the database"
        logger.info(message)
        return ErrorResponseModel(403, message)
    else:
        new_equipment = await add(equipment)
        logger.info(f"Equipment: {equipment.name}  -  added to the database")
        return ResponseModel(201, new_equipment, "Equipment added successfully")


@router.delete(
    "/equipment/{equipment_id}",
    tags=["equipment"],
    summary="Delete equipment",
    description="Delete an equipment specified by it's ObjectId",
    response_model=Response,
)
async def delete_equipment(equipment_id: str):
    """Удаляем обьект equipment из бд"""

    # Проверка на правильность ObjectId
    id = check_ObjectId(equipment_id)

    if id:
        if await get(id):
            await remove(id)
            message = f"Equipment: {equipment_id}  -  deleted from the database"
            logger.info(message)
            return ResponseModel(200, message, "Equipment deleted successfully")
        else:
            message = f"Equipment: {equipment_id}  -  not found in the database"
            logger.info(message)
            return ErrorResponseModel(404, message)
    else:
        message = "ObjectId is written in the wrong format"
        return ErrorResponseModel(400, message)


@router.patch(
    "/equipment/{equipment_id}",
    tags=["equipment"],
    summary="Patch equipment",
    description="Updates additional atributes of equipment specified by it's ObjectId",
    response_model=Response,
)
async def patch_equipment(equipment_id: str, new_values: dict) -> str:
    """Обновляем необязательные поля в equipment в бд"""

    # Проверка на правильность ObjectId
    id = check_ObjectId(equipment_id)

    if id:
        if await get(id):
            await patch_additional(id, new_values)
            message = f"Equipment: {equipment_id}  -  pached"
            logger.info(
                message
            )  # Если ключа нет в обьекте, то будет добавлена новая пара ключ-значение к этому обьекту
            return ResponseModel(200, message, "Equipment patched successfully")
        else:
            message = f"Equipment: {equipment_id}  -  not found in the database"
            logger.info(message)
            return ErrorResponseModel(404, message)
    else:
        message = "ObjectId is written in the wrong format"
        return ErrorResponseModel(400, message)


@router.put(
    "/equipment/{equipment_id}",
    tags=["equipment"],
    summary="Update equipment",
    description="Deletes old atributes of equipment specified by it's ObjectId and puts in new ones",
    response_model=Response,
)
async def update_equipment(equipment_id: str, new_values: Equipment):
    """Обновляем/добавляем поле/поля в equipment в бд"""

    # Проверка на правильность ObjectId
    id = check_ObjectId(equipment_id)

    if id:
        if await get(id):
            await remove(id)
            await add_empty(id)
            await patch_all(id, new_values)
            message = f"Equipment: {equipment_id}  -  updated"
            logger.info(
                message
            )  # Если ключа нет в обьекте, то будет добавлена новая пара ключ-значение к этому обьекту
            return ResponseModel(200, message, "Equipment updated successfully")
        else:
            message = f"Equipment: {equipment_id}  -  not found in the database"
            logger.info(message)
            return ErrorResponseModel(404, message)
    else:
        message = "ObjectId is written in the wrong format"
        return ErrorResponseModel(400, message)
