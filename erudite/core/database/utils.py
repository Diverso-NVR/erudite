""" Вспомогательные функции """

from bson.objectid import ObjectId

from ..database.models import logger

# Перевод модели в словарь
def mongo_to_dict(obj):
    try:
        id = obj.get("_id")
        return {**obj, "_id": str(obj["_id"])}
    except:
        return {**obj}


# Проверка на правильность формата введенного ObjectId
def check_ObjectId(id: str) -> str:
    try:
        new_id = ObjectId(id)
        return new_id
    except:
        message = "ObjectId is written in the wrong format"
        logger.info(message)
        return False