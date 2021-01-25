from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from loguru import logger
from typing import Optional, List
from datetime import datetime

from pydantic import EmailStr

from ..database.models import Message
from ..database.utils import check_ObjectId, get_not_None_args
from ..database import lessons


router = APIRouter()


@router.get(
    "/lessons",
    summary="Get all lessons or lesson by it's ruz id",
    description=(
        "Get a list of all lessons in the database, or a lessons in specified room and datetime"
    ),
    response_model=List[lessons.Lesson],
)
async def get_lessons(
    ruz_auditorium: Optional[str] = None,
    ruz_auditorium_oid: Optional[int] = None,
    ruz_discipline: Optional[str] = None,
    ruz_discipline_oid: Optional[int] = None,
    ruz_kind_of_work: Optional[str] = None,
    ruz_kind_of_work_oid: Optional[int] = None,
    ruz_lecturer_title: Optional[str] = None,
    ruz_lecturer_email: Optional[EmailStr] = None,
    ruz_lesson_oid: Optional[int] = None,
    ruz_url: Optional[str] = None,
    course_code: Optional[str] = None,
    gcalendar_event_id: Optional[str] = None,
    gcalendar_calendar_id: Optional[str] = None,
    fromdate: Optional[datetime] = None,
    todate: Optional[datetime] = None,
):
    if all(
        p is None
        for p in [
            ruz_auditorium,
            ruz_auditorium_oid,
            ruz_discipline,
            ruz_discipline_oid,
            ruz_kind_of_work,
            ruz_kind_of_work_oid,
            ruz_lecturer_title,
            ruz_lesson_oid,
            ruz_url,
            course_code,
            gcalendar_event_id,
            gcalendar_calendar_id,
            ruz_lecturer_email,
            fromdate,
            todate,
        ]
    ):
        return await lessons.get_all()

    all_args = locals()
    filter_args = get_not_None_args(all_args)

    lessons_found = await lessons.sort_many(filter_args)
    if lessons_found:
        logger.info("Lessons found")
        return lessons_found

    message = "Lessons are not found"
    logger.info(message)
    return JSONResponse(status_code=404, content={"message": message})


@router.get(
    "/lessons/{lesson_id}",
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


@router.put(
    "/lessons/{lesson_id}",
    summary="Updates lesson",
    description="Deletes old atributes of lesson specified by it's ObjectId and puts in new ones",
    response_model=lessons.Lesson,
    responses={400: {"model": Message}, 404: {"model": Message}},
)
async def update_lesson(lesson_id: str, lesson: lessons.Lesson, request: Request):
    # Check if ObjectId is in the right format
    id = check_ObjectId(lesson_id)
    new_values = await request.json()

    if not id:
        message = "ObjectId is written in the wrong format"
        return JSONResponse(status_code=400, content={"message": message})

    if not new_values:
        message = "Please fill the request body"
        return JSONResponse(status_code=400, content={"message": message})

    if await lessons.get_by_id(id):
        await lessons.remove(id)
        await lessons.add_empty(id)
        await lessons.put(id, new_values)
        message = f"Lesson: {lesson_id} updated"
        logger.info(message)
        return await request.json()
    # Check if lesson with specified ObjectId is in the database
    else:
        message = f"Lesson: {lesson_id}  -  not found in the database"
        logger.info(message)
        return JSONResponse(status_code=404, content={"message": message})
