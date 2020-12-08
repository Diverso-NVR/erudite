""" Вспомогательные функции """

import logging

from bson.objectid import ObjectId


logger = logging.getLogger("erudite")


# Перевод модели в словарь
def mongo_to_dict(obj):
    if obj.get("_id") is None:
        return obj

    return {**obj, "_id": str(obj["_id"])}


# Проверка на правильность формата введенного ObjectId
def check_ObjectId(id: str) -> str:
    try:
        new_id = ObjectId(id)
        return new_id
    except Exception:
        message = "ObjectId is written in the wrong format"
        logger.info(message)
        return False
