from ..database.models import Discipline, db
from ..database.utils import mongo_to_dict


disciplines_collection = db.get_collection("disciplines")


async def get_all() -> list:
    """ Достаем дисциплины из бд """

    return [
        mongo_to_dict(discipline) async for discipline in disciplines_collection.find()
    ]


async def get(discipline_id: str) -> Discipline:
    """ Достаем дисциплину по указанному ObjectId из бд """

    discipline = await disciplines_collection.find_one({"_id": discipline_id})
    if discipline:
        return mongo_to_dict(discipline)
    else:
        return False


async def get_by_cource_code(course_code: str) -> dict:
    """ Достаем комнату по указанному имени из бд """

    discipline = await disciplines_collection.find_one({"course_code": course_code})
    if discipline:
        return mongo_to_dict(discipline)
    else:
        return False


async def add(discipline: Discipline) -> dict:
    """ Добавляем комнату в бд """

    discipline_added = await disciplines_collection.insert_one(
        discipline.dict(by_alias=True)
    )
    new = await disciplines_collection.find_one({"_id": discipline_added.inserted_id})
    return mongo_to_dict(new)
