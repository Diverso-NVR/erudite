from loguru import logger
from typing import Dict, Optional, List, Union
from pydantic import BaseModel, Field
from bson.objectid import ObjectId
import datetime

from .models import db
from .utils import mongo_to_dict

lessons_collection = db.get_collection("lessons")


class Lesson(BaseModel):
    schedule_lesson_id: int = Field(
        ..., description="Lesson id from schedule servise", example=7735895
    )
    schedule_auditorium_id: int = Field(
        ..., description="Room id in schedule servise", example=3308
    )

    schedule_course_code: str = Field(
        ...,
        description="Course code parsed from schedule servise",
        example="Ф_Б2019_ИТСС_3",
    )

    start_point: datetime.datetime = Field(
        ...,
        description="Start datetime of the lesson",
        example="2021-06-19 18:10:00",
    )
    end_point: datetime.datetime = Field(
        ...,
        description="End datetime of the lesson",
        example="2021-06-19 18:10:00",
    )

    original: dict = Field(..., description="Original json from the schedule servise (like RUZ)")

    group_emails: list = Field([], description="Emails of groups that are connected to this lesson")

    class Config:
        extra = "allow"


async def get_all() -> List[Dict[str, Union[str, int]]]:
    """ Get all lessons from db """

    return [mongo_to_dict(lesson) async for lesson in lessons_collection.find()]


async def sort_many(attributes: dict) -> Optional[List[Dict[str, Union[str, int]]]]:
    """ Get lesson by its ruz name and datetime or any of it's attributes """

    fromdate = attributes.pop("fromdate", None)
    todate = attributes.pop("todate", None)

    if fromdate:
        attributes["start_point"] = {
            "$gte": fromdate.strftime("%Y-%m-%dT%H:%M:%S"),
        }

    if todate:
        attributes["end_point"] = {
            "$lte": todate.strftime("%Y-%m-%dT%H:%M:%S"),
        }

    logger.info(f"lessons.sort_many got filter obj: {attributes}")

    return [mongo_to_dict(lesson) async for lesson in lessons_collection.find(attributes)]


async def get_by_id(lesson_id: ObjectId) -> Optional[Dict[str, Union[str, int]]]:
    """ Get lesson by its db id """

    lesson = await lessons_collection.find_one({"_id": lesson_id})
    if lesson:
        return mongo_to_dict(lesson)


async def get_by_schedule_id(
    schedule_lesson_id: int,
) -> Optional[Dict[str, Union[str, int]]]:
    """ Get lesson by its id in RUZ """

    lesson = await lessons_collection.find_one({"schedule_lesson_id": schedule_lesson_id})
    if lesson:
        return mongo_to_dict(lesson)


async def add(lesson: dict) -> Dict[str, Union[str, int]]:
    """ Add lesson to db """

    lesson_added = await lessons_collection.insert_one(lesson)
    new = await lessons_collection.find_one({"_id": lesson_added.inserted_id})

    return mongo_to_dict(new)


async def add_empty(lesson_id: ObjectId):
    """ Add empty lesson with specified id to db """

    await lessons_collection.insert_one({"_id": lesson_id})


async def remove(lesson_id: ObjectId):
    """ Delete lesson from db """

    res = await lessons_collection.delete_one({"_id": lesson_id})
    return res


async def put(lesson_id: ObjectId, new_values: dict):
    """ Update lesson """

    await lessons_collection.update_one(
        {"_id": lesson_id},
        {"$set": new_values},
    )
