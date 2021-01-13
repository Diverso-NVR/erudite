from pydantic import BaseModel, Field
from typing import List

from ..database.models import db
from ..database.utils import mongo_to_dict


disciplines_collection = db.get_collection("disciplines")


# Class of disciplines
class Discipline(BaseModel):
    course_code: str = Field(...)
    groups: List[str] = Field(...)
    emails: List[str] = Field(...)

    class Config:
        extra = "allow"


async def get_all() -> list:
    """ Get all disciplines from db """

    return [
        mongo_to_dict(discipline) async for discipline in disciplines_collection.find()
    ]


async def get(discipline_id: str) -> Discipline:
    """ Get discipline by its db id """

    discipline = await disciplines_collection.find_one({"_id": discipline_id})
    if discipline:
        return mongo_to_dict(discipline)


async def get_by_cource_code(course_code: str) -> dict:
    """ Get discipline by its course_code """

    discipline = await disciplines_collection.find_one({"course_code": course_code})
    if discipline:
        return mongo_to_dict(discipline)


async def add(discipline: dict) -> dict:
    """ Add discipline to db """

    discipline_added = await disciplines_collection.insert_one(discipline)
    new = await disciplines_collection.find_one({"_id": discipline_added.inserted_id})
    return mongo_to_dict(new)


async def add_empty(discipline_id: str):
    """ Add empty discipline with specified id to db """

    await disciplines_collection.insert_one({"_id": discipline_id})


async def remove(discipline_id: str):
    """ Delete discipline from db """

    await disciplines_collection.delete_one({"_id": discipline_id})


async def patch_all(discipline_id: str, new_values: Discipline):
    """ Patch discipline """

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
