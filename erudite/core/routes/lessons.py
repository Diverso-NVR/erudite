from fastapi import APIRouter, Request
import logging
from typing import Optional
from datetime import datetime

from ..database.models import ErrorResponseModel, ResponseModel, Response
from ..database.utils import check_ObjectId
from ..database import lessons

router = APIRouter()

logger = logging.getLogger("erudite")


@router.get(
    "/lessons",
    tags=["lessons"],
    summary="Get all lessons or lesson by it's ruz id",
    description=(
        "Get a list of all lessons in the database, or a lesson by it's ruz iz, if provided"
    ),
    response_model=Response,
)
async def get_lessons(
    ruz_auditorium: Optional[str] = None,
    fromdate: Optional[datetime] = None,
    todate: Optional[datetime] = None,
):
    if ruz_auditorium is None and fromdate is None and todate is None:
        return ResponseModel(
            200,
            await lessons.get_all(),
            "All lessons returned successfully",
        )

    lessons_res = await lessons.get_filtered_by_name_and_time(
        ruz_auditorium, fromdate, todate
    )

    return ResponseModel(200, lessons_res, "Filtered lessons returned successfully")


@router.get(
    "/lessons/{lesson_id}",
    tags=["lessons"],
    summary="Get a lesson",
    description="Get a lesson specified by it's ObjectId",
    response_model=Response,
)
async def get_lesson_by_id(lesson_id: str):
    # Check if ObjectId is in the right format
    id = check_ObjectId(lesson_id)
    if not id:
        message = "ObjectId is written in the wrong format"
        return ErrorResponseModel(400, message)

    # Check if lesson with specified ObjectId is in the database
    lesson = await lessons.get_by_id(id)
    if lesson:
        logger.info(f"Lesson {lesson_id}: {lesson}")
        return ResponseModel(200, lesson, "Lesson returned successfully")
    else:
        message = "This lesson is not found"
        logger.info(message)
        return ErrorResponseModel(404, message)


@router.post(
    "/lessons",
    status_code=201,
    tags=["lessons"],
    summary="Create lesson",
    description="Create lesson",
    response_model=Response,
)
async def add_lesson(lesson: lessons.Lesson, request: Request):
    if await lessons.get_by_ruz_id(lesson.ruz_lesson_oid):
        message = f"Lesson with ruz id: {lesson.ruz_lesson_oid}  -  already exists in the database"
        logger.info(message)
        return ErrorResponseModel(409, message)

    new_lesson = await lessons.add(await request.json())

    return ResponseModel(201, new_lesson, "Lesson added")
