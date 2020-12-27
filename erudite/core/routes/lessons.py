from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

import logging
from typing import Optional, List
from datetime import datetime

from ..database.models import Message
from ..database.utils import check_ObjectId
from ..database import lessons

router = APIRouter()

logger = logging.getLogger("erudite")


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
    fromdate: Optional[datetime] = None,
    todate: Optional[datetime] = None,
):
    if ruz_auditorium is None and fromdate is None and todate is None:
        return await lessons.get_all()

    return await lessons.get_filtered_by_name_and_time(ruz_auditorium, fromdate, todate)


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
