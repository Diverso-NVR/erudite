from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from loguru import logger
from typing import Optional, List
from datetime import datetime

from ..database.models import Message
from ..database.utils import check_ObjectId, get_not_None_args
from ..database import records


router = APIRouter()


@router.get(
    "/records",
    summary="Get all records or filtered by query args",
    response_model=List[records.Record],
    responses={404: {"model": Message}},
)
async def get_records(
    fromdate: Optional[datetime] = None,
    todate: Optional[datetime] = None,
    room_name: Optional[str] = None,
    url: Optional[str] = None,
):
    if all(p is None for p in [fromdate, todate, room_name, url]):
        return await records.get_all()

    all_args = locals()
    filter_args = get_not_None_args(all_args)

    records_found = await records.sort_many(filter_args)
    if records_found:
      logger.info(f"Records found: {records_found}")
      return records_found
    
    message = "Records not found"
    logger.info(message)
    return JSONResponse(status_code=404, content={"message": message})

@router.get(
    "/records/{record_id}",
    summary="Get a record",
    description="Get a record specified by it's ObjectId",
    response_model=records.Record,
    responses={400: {"model": Message}, 404: {"model": Message}},
)
async def get_record_by_id(record_id: str):
    # Check if ObjectId is in the right format
    id = check_ObjectId(record_id)
    if not id:
        message = "ObjectId is written in the wrong format"
        return JSONResponse(status_code=400, content={"message": message})

    # Check if record with specified ObjectId is in the database
    record = await records.get_by_id(id)
    if record:
        logger.info(f"Record {record_id}: {record}")
        return record
    else:
        message = "This record is not found"
        logger.info(message)
        return JSONResponse(status_code=404, content={"message": message})


@router.post(
    "/records",
    status_code=201,
    summary="Create record",
    description="Create record",
    response_model=records.Record,
    responses={409: {"model": Message}},
)
async def add_record(record: records.Record, request: Request):
    if await records.get_by_url(record.url):
        message = f"Record with url: {record.url}  -  already exists in the database"
        logger.info(message)
        return JSONResponse(status_code=409, content={"message": message})

    return await records.add(await request.json())

@router.delete(
    "/records/{record_id}",
    summary="Delete record",
    description="Delete record specified by it's id",
    response_model=Message,
    responses={400: {"model": Message}, 404: {"model": Message}},
)
async def delete_record(record_id: str):
    # Check if ObjectId is in the right format
    id = check_ObjectId(record_id)

    if not id:
        message = "ObjectId is written in the wrong format"
        return JSONResponse(status_code=400, content={"message": message})

    # Check if Record with specified ObjectId is in the database
    if await records.get_by_id(id):
        await records.remove(id)
        message = f"Record: {record_id}  -  deleted from the database"
        logger.info(message)
        return {"message": message}

    message = f"Record: {record_id}  -  not found in the database"
    logger.info(message)
    return JSONResponse(status_code=404, content={"message": message})

@router.put(
    "/records/{record_id}",
    summary="Updates record",
    description="Deletes old atributes of record specified by it's ObjectId and puts in new ones",
    response_model=records.Record,
    responses={400: {"model": Message}, 404: {"model": Message}},
)
async def update_record(record_id: str, record: records.Record, request: Request):
    # Check if ObjectId is in the right format
    id = check_ObjectId(record_id)
    new_values = await request.json()

    if not id:
        message = "ObjectId is written in the wrong format"
        return JSONResponse(status_code=400, content={"message": message})

    if not new_values:
        message = "Please fill the request body"
        return JSONResponse(status_code=400, content={"message": message})

    if await records.get_by_id(id):
        await records.remove(id)
        await records.add_empty(id)
        await records.put(id, new_values)
        message = f"Record: {record_id} updated"
        logger.info(message)
        return await request.json()
    # Check if Record with specified ObjectId is in the database
    else:
        message = f"Record: {record_id}  -  not found in the database"
        logger.info(message)
        return JSONResponse(status_code=404, content={"message": message})