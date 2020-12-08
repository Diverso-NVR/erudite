from fastapi import APIRouter
import logging
from typing import Optional

from ..database.models import Discipline, ErrorResponseModel, ResponseModel, Response
from ..database.utils import check_ObjectId
from ..database.disciplines import get_all, get, add, get_by_cource_code

router = APIRouter()

logger = logging.getLogger("erudite")


@router.get(
    "/disciplines",
    tags=["disciplines"],
    summary="Get all disciplines/discipline by it's course code",
    description=(
        "Get a list of all disciplines in the database,"
        "or a discipline by it's course code, if provided"
    ),
    response_model=Response,
)
async def get_disciplines(course_code: Optional[str] = None):
    """Достаем обьект discipline из бд"""

    if course_code is None:
        return ResponseModel(
            200,
            await get_all(),
            "Disciplines returned successfully",
        )

    discipline = await get_by_cource_code(course_code)
    if discipline:
        logger.info(f"Discipline {course_code}: {discipline}")
        return ResponseModel(200, discipline, "Discipline returned successfully")
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
    """Достаем обьект discipline из бд"""

    # Проверка на правильность ObjectId
    id = check_ObjectId(discipline_id)

    # Проверка на наличие правилно введенного ObjectId в БД
    if id:
        discipline = await get(id)
        if discipline:
            logger.info(f"Discipline {discipline_id}: {discipline}")
            return ResponseModel(200, discipline, "Discipline returned successfully")
        else:
            message = "This discipline is not found"
            logger.info(message)
            return ErrorResponseModel(404, message)
    else:
        message = "ObjectId is written in the wrong format"
        return ErrorResponseModel(400, message)


@router.post(
    "/disciplines",
    status_code=201,
    tags=["disciplines"],
    summary="Create discipline",
    description="Create discipline specified by it's ObjectId",
    response_model=Response,
)
async def add_discipline(discipline: Discipline):
    """Создаем обьект discipline"""

    if await get_by_cource_code(discipline.course_code):
        message = f"Discipline with code: {discipline.course_code} already exists in the database"
        logger.info(message)
        return ErrorResponseModel(403, message)

    new_discipline = await add(discipline)

    return ResponseModel(201, new_discipline, "Discipline added")
