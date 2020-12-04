from fastapi import APIRouter
import logging
from typing import Optional

from bson.objectid import ObjectId

from ..db.models import Discipline, db, mongo_to_dict

router = APIRouter()

logger = logging.getLogger("erudite")

disciplines_collection = db.get_collection("disciplines")


@router.get("/disciplines", tags=["disciplines"])
async def find_discipline(course_code: Optional[str] = None):
    """Достаем обьект discipline из бд"""

    if course_code is None:
        return [mongo_to_dict(discipline) async for discipline in disciplines_collection.find()]

    discipline = await disciplines_collection.find_one({"course_code": course_code})
    if discipline:
        logger.info(f"Discipline {course_code}: {discipline}")
        return mongo_to_dict(discipline)
    else:
        logger.info("This discipline is not found")
        return {}


@router.get("/disciplines/{discipline_id}", tags=["disciplines"])
async def find_discipline(discipline_id: str):
    """Достаем обьект discipline из бд"""

    discipline = await disciplines_collection.find_one({"_id": ObjectId(discipline_id)})
    if discipline:
        logger.info(f"Discipline {discipline_id}: {discipline}")
        return mongo_to_dict(discipline)
    else:
        logger.info("This discipline is not found")
        return {}


@router.post("/disciplines", status_code=201, tags=["disciplines"])
async def add_discipline(discipline: Discipline):
    if await disciplines_collection.find_one({"course_code": discipline.course_code}):
        logger.info(f"Discipline with code: {discipline.course_code}  -  already exists in the database")
        return {}

    discipline_added = await disciplines_collection.insert_one(discipline.dict(by_alias=True))
    new_discipline = await disciplines_collection.find_one({"_id": discipline_added.inserted_id})

    return {"message": "Discipline added", "discipline": mongo_to_dict(new_discipline)}
