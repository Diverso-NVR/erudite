from fastapi import APIRouter
import logging
from bson.objectid import ObjectId

from ..db.models import Equipment, db, mongo_to_dict, ErrorResponseModel, ResponseModel, Response, mongo_to_dict_no_id

router = APIRouter()

logger = logging.getLogger("erudite")

equipment_collection = db.get_collection("equipment")


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
        [mongo_to_dict(equipment) async for equipment in equipment_collection.find()],
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
    try:
        id = ObjectId(equipment_id)
    except:
        message = "ObjectId is written in the wrong format"
        logger.info(message)
        return ErrorResponseModel(400, message)

    # Проверка на наличие правилно введенного ObjectId в БД
    equipment = await equipment_collection.find_one({"_id": id})
    if equipment:
        logger.info(f"Equipment {equipment_id}: {equipment}")
        return ResponseModel(200, mongo_to_dict(equipment), "Room returned successfully")
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
async def create_equipment(equipment: Equipment):
    """Добавляем обьект equipment в бд"""

    if await equipment_collection.find_one({"name": equipment.name}):
        message = f"Equipment with name: '{equipment.name}'  -  already exists in the database"
        logger.info(message)
        return ErrorResponseModel(403, message)
    else:
        equipment_added = await equipment_collection.insert_one(equipment.dict(by_alias=True))
        new_equipment = await equipment_collection.find_one({"_id": equipment_added.inserted_id})
        logger.info(f"Equipment: {equipment.name}  -  added to the database")
        return ResponseModel(201, mongo_to_dict(new_equipment), "Equipment added successfully")


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
    try:
        id = ObjectId(equipment_id)
    except:
        message = "ObjectId is written in the wrong format"
        logger.info(message)
        return ErrorResponseModel(400, message)

    if await equipment_collection.find_one({"_id": id}):
        await equipment_collection.delete_one({"_id": id})
        message = f"Equipment: {equipment_id}  -  deleted from the database"
        logger.info(message)
        return ResponseModel(200, message, "Equipment deleted successfully")
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
    """Обновляем необязательные поля в equipment в бд"""

    # Проверка на правильность ObjectId
    try:
        id = ObjectId(equipment_id)
    except:
        message = "ObjectId is written in the wrong format"
        logger.info(message)
        return ErrorResponseModel(400, message)

    if await equipment_collection.find_one({"_id": id}):
        await equipment_collection.update_one({"_id": id}, {"$set": {"additional": new_values}})
        message = f"Equipment: {equipment_id}  -  pached"
        logger.info(message)  # Если ключа нет в обьекте, то будет добавлена новая пара ключ-значение к этому обьекту
        return ResponseModel(200, message, "Equipment patched successfully")
    else:
        message = f"Equipment: {equipment_id}  -  not found in the database"
        logger.info(message)
        return ErrorResponseModel(404, message)


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
    try:
        id = ObjectId(equipment_id)
    except:
        message = "ObjectId is written in the wrong format"
        logger.info(message)
        return ErrorResponseModel(400, message)

    if await equipment_collection.find_one({"_id": id}):
        await equipment_collection.delete_one({"_id": id})
        await equipment_collection.insert_one({"_id": id})
        await equipment_collection.update_one(
            {"_id": id},
            {
                "$set": {
                    "name": new_values.name,
                    "type": new_values.type,
                    "additional": mongo_to_dict_no_id(new_values.additional),
                }
            },
        )
        message = f"Equipment: {equipment_id}  -  updated"
        logger.info(message)  # Если ключа нет в обьекте, то будет добавлена новая пара ключ-значение к этому обьекту
        return ResponseModel(200, message, "Equipment updated successfully")
    else:
        message = f"Equipment: {equipment_id}  -  not found in the database"
        logger.info(message)
        return ErrorResponseModel(404, message)
