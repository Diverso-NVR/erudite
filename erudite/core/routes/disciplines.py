from fastapi import APIRouter
import logging
from typing import Optional

from ..database.models import ErrorResponseModel, ResponseModel, Response
from ..database.utils import check_ObjectId
from ..database import disciplines

router = APIRouter()

logger = logging.getLogger("erudite")


@router.get(
    "/disciplines",
    tags=["disciplines"],
    summary="Get all disciplines/discipline by it's course code",
    description=(
        "Get a list of all disciplines in the database, or a discipline by it's course code"
    ),
    response_model=Response,
)
async def get_disciplines(course_code: Optional[str] = None):
    if course_code is None:
        return ResponseModel(
            200,
            await disciplines.get_all(),
            "Disciplines returned successfully",
        )

    discipline = await disciplines.get_by_cource_code(course_code)
    if discipline:
        logger.info(f"Discipline {course_code}: {discipline}")
        return ResponseModel(200, discipline, "Discipline returned successfully")
    # Check if discipline with specified ObjectId is in the database
    else:
        message = "This discipline is not found"
        logger.info(message)
        return ErrorResponseModel(404, message)


@router.get(
    "/disciplines/{discipline_id}",
    tags=["disciplines"],
    summary="Get a discipline",
    description="Get a discipline specified by it's ObjectId",
    response_model=Response,
)
async def find_discipline(discipline_id: str):
    # Check if ObjectId is in the right format
    id = check_ObjectId(discipline_id)

    # Check if discipline with specified ObjectId is in the database
    if not id:
        message = "ObjectId is written in the wrong format"
        return ErrorResponseModel(400, message)

    discipline = await disciplines.get(id)
    if discipline:
        logger.info(f"Discipline {discipline_id}: {discipline}")
        return ResponseModel(200, discipline, "Discipline returned successfully")
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
    response_model=Response,
)
async def add_discipline(discipline: disciplines.Discipline):
    # Check if discipline with specified ObjectId is in the database
    if await disciplines.get_by_cource_code(discipline.course_code):
        message = f"Discipline with code: {discipline.course_code} already exists in the database"
        logger.info(message)
        return ErrorResponseModel(409, message)

    new_discipline = await disciplines.add(discipline)

    return ResponseModel(201, new_discipline, "Discipline added")


@router.delete(
    "/disciplines/{discipline_id}",
    tags=["disciplines"],
    summary="Delete discipline",
    description="Delete discipline specified by it's ObjectId",
    response_model=Response,
)
async def delete_discipline(discipline_id: str):
    # Check if ObjectId is in the right format
    id = check_ObjectId(discipline_id)

    if not id:
        message = "ObjectId is written in the wrong format"
        return ErrorResponseModel(400, message)

    if await disciplines.get(id):
        await disciplines.remove(id)
        message = f"Discipline: {discipline_id}  -  deleted from the database"
        logger.info(message)
        return ResponseModel(200, message, "Room deleted successfully")
    # Check if discipline with specified ObjectId is in the database
    else:
        message = f"Discipline: {discipline_id}  -  not found in the database"
        logger.info(message)
        return ErrorResponseModel(404, message)


@router.put(
    "/disciplines/{discipline_id}",
    tags=["disciplines"],
    summary="Updates discipline",
    description=(
        "Deletes old atributes of discipline specified by it's ObjectId and puts in new ones"
    ),
    response_model=Response,
)
async def update_discipline(discipline_id: str, new_values: disciplines.Discipline):
    # Check if ObjectId is in the right format
    id = check_ObjectId(discipline_id)

    if not id:
        message = "ObjectId is written in the wrong format"
        return ErrorResponseModel(400, message)

    if await disciplines.get(id):
        await disciplines.remove(id)
        await disciplines.add_empty(id)
        await disciplines.patch_all(id, new_values)
        message = f"Discipline: {discipline_id}  -  updated"
        logger.info(
            message
        )  # Если ключа нет в обьекте, то будет добавлена новая пара ключ-значение к этому обьекту
        return ResponseModel(200, message, "Discipline updated successfully")
    # Check if discipline with specified ObjectId is in the database
    else:
        message = f"Discipline: {discipline_id}  -  not found in the database"
        logger.info(message)
        return ErrorResponseModel(404, message)
