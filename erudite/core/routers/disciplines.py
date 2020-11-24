from fastapi import APIRouter
import logging

from ..db.models import Discipline, db, mongo_to_dict

router = APIRouter()

logger = logging.getLogger("erudite")

disciplines_collection = db.get_collection("disciplines")


@router.get("/disciplines")
async def list_disciplines():
    """Достаем все disciplines"""
    return [
        mongo_to_dict(discipline) async for discipline in disciplines_collection.find()
    ]


@router.post("/disciplines", status_code=201)
async def add_discipline(discipline: Discipline):
    if await disciplines_collection.find_one({"course_code": discipline.course_code}):
        logger.info(
            f"Discipline with code: {discipline.course_code}  -  already exists in the database"
        )
        return {}

    discipline_added = await disciplines_collection.insert_one(
        discipline.dict(by_alias=True)
    )
    new_discipline = await disciplines_collection.find_one(
        {"_id": discipline_added.inserted_id}
    )

    return {"message": "Discipline added", "discipline": mongo_to_dict(new_discipline)}
