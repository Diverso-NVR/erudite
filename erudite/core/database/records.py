from loguru import logger
from typing import Dict, Optional, List, Union
from pydantic import BaseModel, Field
from bson.objectid import ObjectId

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

    class Config:
        extra = "allow"


async def get_all() -> List[Dict[str, str]]:
    return [mongo_to_dict(record) async for record in records_collection.find()]


async def get_by_url(url: str) -> Optional[Dict[str, Union[str, int]]]:
    record = await records_collection.find_one({"url": url})
    if record:
        return mongo_to_dict(record)


async def sort_many(attributes: dict) -> Optional[List[Dict[str, str]]]:
    fromdate = attributes.pop("fromdate", None)
    todate = attributes.pop("todate", None)

    if fromdate is not None:
        attributes["date"] = {
            "$gte": str(fromdate.date()),
        }
        attributes["start_time"] = {"$gte": str(fromdate.time())}

    if todate is not None:
        attributes.setdefault("date", {})
        attributes["date"]["$lte"] = str(todate.date())

        attributes.setdefault("start_time", {})
        attributes["start_time"]["$lte"] = str(todate.time())

    logger.info(f"records.sort_many got filter obj: {attributes}")

    return [
        mongo_to_dict(record) async for record in records_collection.find(attributes)
    ]


async def get_by_id(record_id: ObjectId) -> Optional[Dict[str, str]]:
    record = await records_collection.find({"_id": record_id})
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
