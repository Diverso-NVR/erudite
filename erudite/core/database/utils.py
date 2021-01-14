""" Вспомогательные функции """

from loguru import logger

from bson.objectid import ObjectId


# Schemas to dictionary
def mongo_to_dict(obj):
    if obj.get("_id") is None:
        return obj

    res = {"id": str(obj["_id"]), **obj}
    res.pop("_id")

    return res


# Check if ObjectId is in the right format
def check_ObjectId(id: str) -> ObjectId:
    try:
        new_id = ObjectId(id)
        return new_id
    except Exception:
        message = "ObjectId is written in the wrong format"
        logger.info(message)
        return False


# Get all arguments from a function witch are not None
def get_not_None_args(all_args: dict) -> dict:
    filter_list = {
        element: all_args[element]
        for element in all_args
        if all_args[element] is not None
    }
    del all_args

    return filter_list
