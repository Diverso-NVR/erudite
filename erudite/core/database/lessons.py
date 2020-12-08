from typing import Dict, Optional, List, Union
from pydantic import BaseModel, Field

from .models import db
from .utils import mongo_to_dict

lessons_collection = db.get_collection("lessons")


class Lesson(BaseModel):
    ruz_auditorium: str = Field(..., description="Room name in RUZ", example="104")
    ruz_auditorium_oid: int = Field(..., description="Room id in RUZ", example=3308)
    ruz_building: str = Field(
        ...,
        description="Building in which room is located",
        example="Таллинская ул., д, 34",
    )
    ruz_building_oid: int = Field(
        ..., description="Building id in which room is located", example=2211
    )
    ruz_discipline: str = Field(
        ..., description="Discipline name in RUZ", example="Физика"
    )
    ruz_discipline_oid: int = Field(
        ..., description="Discipline id in RUZ", example=1337
    )
    ruz_kind_of_work: str = Field(
        ...,
        description="Lesson type name from RUZ",
        example="Практическое занятие on-line",
    )
    ruz_kind_of_work_oid: int = Field(
        ..., description="Lesson type id from RUZ", example=969
    )
    ruz_lecturer_title: str = Field(
        ..., description="Lecturer name from RUZ", example="Даниил Мирталибов"
    )
    ruz_lecturer_email: str = Field(
        ..., description="Lecturer email from RUZ", example="dimirtalibov@hse.ru"
    )
    ruz_lesson_oid: int = Field(..., description="Lesson id from RUZ", example=7735895)
    ruz_url: str = Field(
        None,
        description="If lesson is online, than this field will have url to lesson room",
        example="https://meet.miem.hse.ru/520",
    )

    course_code: str = Field(
        ..., description="Course code parsed from RUZ", example="Ф_Б2019_ИТСС_3"
    )
    gcalendar_event_id: str = Field(
        None,
        description="Google Calendar event id. Event is a copy of ruz lesson",
    )
    date: str = Field(..., description="Date of the lesson", example="2020-12-15")
    start_time: str = Field(..., description="Start time of the lesson", example="9:30")
    end_time: str = Field(..., description="End time of the lesson", example="10:50")


async def get_all() -> List[Lesson]:
    """ Get all lessons from db"""

    return [mongo_to_dict(lesson) async for lesson in lessons_collection.find()]


async def get_by_ruz_id(lesson_ruz_id: int) -> Optional[Dict[str, Union[str, int]]]:
    """Get lesson by its ruz id"""

    lesson = await lessons_collection.find_one({"ruz_lesson_oid": int(lesson_ruz_id)})
    if lesson:
        return mongo_to_dict(lesson)


async def get_by_id(lesson_id: str) -> Optional[Dict[str, Union[str, int]]]:
    """Get lesson by its db id"""

    lesson = await lessons_collection.find_one({"_id": lesson_id})
    if lesson:
        return mongo_to_dict(lesson)


async def add(data: dict) -> Dict[str, Union[str, int]]:
    """ Add lesson to db """

    lesson_added = await lessons_collection.insert_one(data)
    new = await lessons_collection.find_one({"_id": lesson_added.inserted_id})

    return mongo_to_dict(new)
