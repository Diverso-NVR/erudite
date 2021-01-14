from loguru import logger
from typing import Optional, List

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from ..database.models import Message
from ..database.utils import check_ObjectId
from ..database import disciplines


router = APIRouter()


@router.get(
    "/disciplines",
    tags=["disciplines"],
    summary="Get all disciplines/discipline by it's course code",
    description=(
        "Get a list of all disciplines in the database, or a discipline by it's course code"
    ),
    response_model=List[disciplines.Discipline],
    responses={404: {"model": Message}},
)
async def get_disciplines(course_code: Optional[str] = None):
    if course_code is None:
        return await disciplines.get_all()

    discipline = await disciplines.get_by_cource_code(course_code)
    if discipline:
        logger.info(f"Discipline {course_code}: {discipline}")
        return [discipline]
    else:
        message = "This discipline is not found"
        logger.info(message)
        return JSONResponse(status_code=404, content={"message": message})


@router.get(
    "/disciplines/{discipline_id}",
    tags=["disciplines"],
    summary="Get a discipline",
    description="Get a discipline specified by it's ObjectId",
    response_model=disciplines.Discipline,
    responses={404: {"model": Message}, 400: {"model": Message}},
)
async def find_discipline(discipline_id: str):
    # Check if ObjectId is in the right format
    id = check_ObjectId(discipline_id)

    # Check if discipline with specified ObjectId is in the database
    if not id:
        message = "Invalid id"
        logger.info(message)
        return JSONResponse(status_code=404, content={"message": message})

    discipline = await disciplines.get(id)
    if discipline:
        logger.info(f"Discipline {discipline_id}: {discipline}")
        return discipline
    else:
        message = "This discipline is not found"
        logger.info(message)
        return JSONResponse(status_code=404, content={"message": message})


@router.post(
    "/disciplines",
    status_code=201,
    tags=["disciplines"],
    summary="Create discipline",
    description="Create discipline specified by it's ObjectId",
    response_model=disciplines.Discipline,
    responses={409: {"model": Message}},
)
async def add_discipline(discipline: disciplines.Discipline, request: Request):
    # Check if discipline with specified ObjectId is in the database
    if await disciplines.get_by_cource_code(discipline.course_code):
        message = f"Discipline with code: {discipline.course_code} already exists in the database"
        logger.info(message)
        return JSONResponse(status_code=409, content={"message": message})

    return await disciplines.add(await request.json())


@router.delete(
    "/disciplines/{discipline_id}",
    tags=["disciplines"],
    summary="Delete discipline",
    description="Delete discipline specified by it's ObjectId",
    response_model=Message,
    responses={400: {"model": Message}, 404: {"model": Message}},
)
async def delete_discipline(discipline_id: str):
    # Check if ObjectId is in the right format
    id = check_ObjectId(discipline_id)

    if not id:
        message = "ObjectId is written in the wrong format"
        return JSONResponse(status_code=400, content={"message": message})

    if await disciplines.get(id):
        await disciplines.remove(id)
        message = f"Discipline: {discipline_id} deleted from the database"
        logger.info(message)
        return {"message": "Room deleted successfully"}
    else:
        message = f"Discipline: {discipline_id} not found in the database"
        logger.info(message)
        return JSONResponse(status_code=404, content={"message": message})


@router.put(
    "/disciplines/{discipline_id}",
    tags=["disciplines"],
    summary="Updates discipline",
    description=(
        "Deletes old atributes of discipline specified by it's ObjectId and puts in new ones"
    ),
    response_model=Message,
    responses={400: {"model": Message}, 404: {"model": Message}},
)
async def update_discipline(
    discipline_id: str, discipline: disciplines.Discipline, request: Request
):
    # Check if ObjectId is in the right format
    id = check_ObjectId(discipline_id)

    if not id:
        message = "ObjectId is written in the wrong format"
        return JSONResponse(status_code=400, content={"message": message})

    if await disciplines.get(id):
        await disciplines.remove(id)
        await disciplines.add_empty(id)
        await disciplines.patch_all(id, await request.json())
        message = f"Discipline: {discipline_id}  -  updated"
        logger.info(
            message
        )  # Если ключа нет в обьекте, то будет добавлена новая пара ключ-значение к этому обьекту
        return message

    else:
        message = f"Discipline: {discipline_id}  -  not found in the database"
        logger.info(message)
        return JSONResponse(status_code=404, content={"message": message})
