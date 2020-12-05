from fastapi import APIRouter
import logging
from typing import Optional

from bson.objectid import ObjectId

from ..db.models import Discipline, db, mongo_to_dict, ErrorResponseModel, ResponseModel

router = APIRouter()

logger = logging.getLogger("erudite")

disciplines_collection = db.get_collection("disciplines")


@router.get(
    "/disciplines",
    tags=["disciplines"],
    summary="Get all disciplines",
    description="Get a list of all disciplines in the database",
)
async def find_discipline(course_code: Optional[str] = None):
    """Достаем обьект discipline из бд"""

    if course_code is None:
        return ResponseModel(
            [mongo_to_dict(discipline) async for discipline in disciplines_collection.find()],
            "Disciplines returned successfully",
        )

    discipline = await disciplines_collection.find_one({"course_code": course_code})
    if discipline:
        logger.info(f"Discipline {course_code}: {discipline}")
        return ResponseModel(mongo_to_dict(discipline), "Discipline returned successfully")
    else:
        message = "This discipline is not found"
        logger.info(message)
        return ErrorResponseModel(404, message)


@router.get(
    "/disciplines/{discipline_id}",
    tags=["disciplines"],
    summary="Get a discipline",
    description="Get a discipline specified by it's ObjectId",
)
async def find_discipline(discipline_id: str):
    """Достаем обьект discipline из бд"""

    # Проверка на правильность ObjectId
    try:
        id = ObjectId(discipline_id)
    except:
        message = "ObjectId is written in the wrong format"
        logger.info(message)
        return ErrorResponseModel(400, message)

    # Проверка на наличие правилно введенного ObjectId в БД
    discipline = await disciplines_collection.find_one({"_id": id})
    if discipline:
        logger.info(f"Discipline {discipline_id}: {discipline}")
        return ResponseModel(mongo_to_dict(discipline), "Discipline returned successfully")
    else:
        message = "This discipline is not found"
        logger.info(message)
        return ErrorResponseModel(404, message)


@router.post(
    "/disciplines",
    status_code=201,
    tags=["disciplines"],
    summary="Create discipline",
    description="Create discipline specified by it's ObjectId",
)
async def add_discipline(discipline: Discipline):
    if await disciplines_collection.find_one({"course_code": discipline.course_code}):
        message = f"Discipline with code: {discipline.course_code}  -  already exists in the database"
        logger.info(message)
        return ErrorResponseModel(403, message)

    discipline_added = await disciplines_collection.insert_one(discipline.dict(by_alias=True))
    new_discipline = await disciplines_collection.find_one({"_id": discipline_added.inserted_id})

    return ResponseModel(mongo_to_dict(new_discipline), "Discipline added")
