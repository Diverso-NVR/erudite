from loguru import logger
from typing import Dict, Optional, List, Union
from pydantic import BaseModel, Field
from bson.objectid import ObjectId
from datetime import timedelta, datetime

from .models import db
from .utils import mongo_to_dict

records_collection = db.get_collection("records")


class Record(BaseModel):
    room_name: str = Field(..., description="Room where record was captured")
    date: str = Field(..., description="Date of record", example="2020-09-01")
    start_time: str = Field(..., description="Start time of record", example="13:00")
    end_time: str = Field(..., description="End time of record", example="13:30")

    type: str = Field(
        None,
        description="Type of record. Also means service. Like Jitsi, Zoom, MS Teams, Offline",
        example="Jitsi",
    )
    url: str = Field(None, description="Record url")
    emotions_url: str = Field(None, description="Emotions graph for record")

    keywords: List[str] = Field(None, description="Keywords from record audio")

    class Config:
        extra = "allow"


rec_types = ["Jitsi", "MS Teams", "Offline", "Autorecord"]


async def get_all(
    page_number: int,
    page_size: int = 50,
    with_keywords_only: bool = False,
    ignore_autorec: bool = False,
) -> List[Dict[str, str]]:
    attributes = {}
    if ignore_autorec:
        attributes["type"] = {"$in": rec_types[:-1]}
    if with_keywords_only:
        attributes["keywords"] = {"$type": "array", "$not": {"$size": 0}}

    return [
        mongo_to_dict(record)
        async for record in records_collection.find(attributes)
        .sort("_id", 1)
        .sort("date", -1)
        .skip(page_number * page_size if page_number > 0 else 0)
        .limit(page_size)
    ]


async def get_by_url(url: str) -> Optional[Dict[str, Union[str, int]]]:
    record = await records_collection.find_one({"url": url})
    if record:
        return mongo_to_dict(record)


async def sort_many(
    attributes: dict,
    page_number: int,
    page_size: int = 50,
    with_keywords_only: bool = False,
    ignore_autorec: bool = False,
) -> Optional[List[Dict[str, str]]]:
    fromdate = attributes.pop("fromdate", None)
    todate = attributes.pop("todate", None)

    if fromdate:
        attributes["end_point"] = {"$gte": str(fromdate)}

    if todate:
        attributes["start_point"] = {"$lte": str(todate)}

    if fromdate and todate:
        attributes.pop("end_point", None)
        attributes.setdefault("$or", [])

        attributes["$or"].append(
            {
                "$and": [
                    {"end_point": {"$gte": str(fromdate)}},
                    {"end_point": {"$lte": str(todate)}},
                ]
            }
        )
        attributes["$or"].append(
            {
                "$and": [
                    {"end_point": {"$gte": str(todate)}},
                    {"start_point": {"$lte": str(fromdate)}},
                ]
            }
        )
        attributes["$or"].append(
            {
                "$and": [
                    {"start_point": {"$gte": str(fromdate)}},
                    {"start_point": {"$lte": str(fromdate)}},
                ]
            }
        )

    logger.info(
        f"records.sort_many got filter obj: {attributes}, page_number: {page_number}, page_size: {page_size}, "
        f"ignore_autorec: {ignore_autorec}, with_keywords_only: {with_keywords_only}"
    )

    if ignore_autorec:
        attributes["type"] = {"$in": rec_types[:-1]}
    if with_keywords_only:
        attributes["keywords"] = {"$type": "array", "$not": {"$size": 0}}

    return [
        mongo_to_dict(record)
        async for record in records_collection.find(attributes)
        .sort("_id", 1)
        .skip(page_number * page_size if page_number > 0 else 0)
        .limit(page_size)
    ]


async def get_by_id(record_id: ObjectId) -> Optional[Dict[str, str]]:
    record = await records_collection.find_one({"_id": record_id})
    if record:
        return mongo_to_dict(record)


async def add(record: Dict[str, str]) -> Dict[str, str]:
    record_added = await records_collection.insert_one(record)
    new_record = await records_collection.find_one({"_id": record_added.inserted_id})

    return mongo_to_dict(new_record)


async def add_empty(record_id: ObjectId):
    await records_collection.insert_one({"_id": record_id})


async def remove(record_id: ObjectId):
    await records_collection.delete_one({"_id": record_id})


async def patch(record_id: ObjectId, new_values: Dict[str, str]):
    await records_collection.update_one({"_id": record_id}, {"$set": new_values})
