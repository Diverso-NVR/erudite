from pydantic import BaseModel, Field
from typing import Optional, List, Dict

from ..database.models import db
from ..database.utils import mongo_to_dict


disciplines_collection = db.get_collection("disciplines")

# Класс дисциплин
class Discipline(BaseModel):
    course_code: str = Field(...)
    groups: List[str] = Field(...)
    emails: List[str] = Field(...)


async def get_all() -> list:
    """ Достаем дисциплины из бд """

    return [mongo_to_dict(discipline) async for discipline in disciplines_collection.find()]


async def get(discipline_id: str) -> Discipline:
    """ Достаем дисциплину по указанному ObjectId из бд """

    discipline = await disciplines_collection.find_one({"_id": discipline_id})
    if discipline:
        return mongo_to_dict(discipline)
    else:
        return False


async def get_by_cource_code(course_code: str) -> dict:
    """ Достаем дисциплину по указанному имени из бд """

    discipline = await disciplines_collection.find_one({"course_code": course_code})
    if discipline:
        return mongo_to_dict(discipline)
    else:
        return False


async def add(discipline: Discipline) -> dict:
    """ Добавляем дисциплину в бд """

    discipline_added = await disciplines_collection.insert_one(discipline.dict(by_alias=True))
    new = await disciplines_collection.find_one({"_id": discipline_added.inserted_id})
    return mongo_to_dict(new)


async def add_empty(discipline_id: str):
    """ Добавляем дисциплину в бд с указанным id """

    await disciplines_collection.insert_one({"_id": discipline_id})


async def remove(discipline_id: str):
    """ Удаляем дисциплину из бд """

    await disciplines_collection.delete_one({"_id": discipline_id})


async def patch_all(discipline_id: str, new_values: Discipline):
    """ Патчим всю дисциплину """

    await disciplines_collection.update_one(
        {"_id": discipline_id},
        {
            "$set": {
                "course_code": new_values.course_code,
                "groups": new_values.groups,
                "emails": new_values.emails,
            }
        },
    )
