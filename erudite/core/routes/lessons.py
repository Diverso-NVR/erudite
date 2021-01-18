from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from loguru import logger
from typing import Optional, List
from datetime import datetime

from pydantic import EmailStr

from ..database.models import Message
from ..database.utils import check_ObjectId
from ..database import lessons


router = APIRouter()


@router.get(
    "/lessons",
    tags=["lessons"],
    summary="Get all lessons or lesson by it's ruz id",
    description=(
        "Get a list of all lessons in the database, or a lessons in specified room and datetime"
    ),
    response_model=List[lessons.Lesson],
)
async def get_lessons(
    ruz_auditorium: Optional[str] = None,
    ruz_lecturer_email: Optional[EmailStr] = None,
    fromdate: Optional[datetime] = None,
    todate: Optional[datetime] = None,
):
    if all(p is None for p in [ruz_auditorium, ruz_lecturer_email, fromdate, todate]):
        return await lessons.get_all()

    return await lessons.get_filtered(ruz_auditorium, ruz_lecturer_email, fromdate, todate)


@router.get(
    "/lessons/{lesson_id}",
    tags=["lessons"],
    summary="Get a lesson",
    description="Get a lesson specified by it's ObjectId",
    response_model=lessons.Lesson,
    responses={400: {"model": Message}, 404: {"model": Message}},
)
async def get_lesson_by_id(lesson_id: str):
    # Check if ObjectId is in the right format
    id = check_ObjectId(lesson_id)
    if not id:
        message = "ObjectId is written in the wrong format"
        return JSONResponse(status_code=400, content={"message": message})

    # Check if lesson with specified ObjectId is in the database
    lesson = await lessons.get_by_id(id)
    if lesson:
        logger.info(f"Lesson {lesson_id}: {lesson}")
        return lesson
    else:
        message = "This lesson is not found"
        logger.info(message)
        return JSONResponse(status_code=404, content={"message": message})


@router.post(
    "/lessons",
    status_code=201,
    tags=["lessons"],
    summary="Create lesson",
    description="Create lesson",
    response_model=lessons.Lesson,
    responses={409: {"model": Message}},
)
async def add_lesson(lesson: lessons.Lesson, request: Request):
    if await lessons.get_by_ruz_id(lesson.ruz_lesson_oid):
        message = f"Lesson with ruz id: {lesson.ruz_lesson_oid}  -  already exists in the database"
        logger.info(message)
        return JSONResponse(status_code=409, content={"message": message})

    return await lessons.add(await request.json())


@router.delete(
    "/lessons/{lesson_id}",
    tags=["lessons"],
    summary="Delete lesson",
    description="Delete lesson specified by it's id",
    response_model=Message,
    responses={400: {"model": Message}, 404: {"model": Message}},
)
async def delete_lesson(lesson_id: str):
    # Check if ObjectId is in the right format
    id = check_ObjectId(lesson_id)

    if not id:
        message = "ObjectId is written in the wrong format"
        return JSONResponse(status_code=400, content={"message": message})

    # Check if lesson with specified ObjectId is in the database
    if await lessons.get_by_id(id):
        await lessons.remove(id)
        message = f"Lesson: {lesson_id}  -  deleted from the database"
        logger.info(message)
        return {"message": message}

    message = f"Lesson: {lesson_id}  -  not found in the database"
    logger.info(message)
    return JSONResponse(status_code=404, content={"message": message})
