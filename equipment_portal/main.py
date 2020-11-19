from fastapi import FastAPI
import motor.motor_asyncio
import os
import logging

from db.models import Equipment, Room

# Достаем uri для доступа к удаленной БД
MONGO_DATABASE_URI = "mongodb://equipment_user:massivePassw0rd28@host1.miem.vmnet.top:20005/test"  # os.environ.get('MONGO_DATABASE_URI')

# Для подключения к внешней БД:
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DATABASE_URI)

# Проверка на тест
TESTING = os.environ.get("TESTING")

# Доступ к БД через motor
if TESTING:
    db = client["testDb"]
else:
    db = client["Equipment"]

# функция логгера
def create_logger(mode="INFO"):
    logs = {"INFO": logging.INFO, "DEBUG": logging.DEBUG}

    logger = logging.getLogger("equipment_portal")
    logger.setLevel(logs[mode])

    handler = logging.StreamHandler()
    handler.setLevel(logs[mode])

    formatter = logging.Formatter("%(levelname)-8s  %(asctime)s    %(message)s", datefmt="%d-%m-%Y %I:%M:%S %p")

    handler.setFormatter(formatter)

    logger.addHandler(handler)


create_logger()  # Создание логгера
logger = logging.getLogger("equipment_portal")  # инициализация логгера

app = FastAPI()


@app.get("/equipment")
async def list_equipments():
    """Достаем все equipment"""

    equipment_list = []
    async for equipment in db.equipment.find():
        equipment_list.append(Equipment(**equipment))
    logger.info(f"Equipment in the database: {equipment_list}")
    return {"equipment": equipment_list}


@app.get("/room")
async def list_rooms():
    """Достаем все rooms"""

    rooms_list = []
    async for room in db.rooms.find():
        rooms_list.append(Room(**room))
    logger.info(f"All rooms in the database: {rooms_list}")
    return rooms_list


@app.get("/room_equipment/{room_id}")
async def list_room_equipments(room_id: int):
    """Достаем все equipment из конкретной комнаты"""

    equipment_list = []
    async for equipment in db.equipment.find({"room_id": room_id}):
        equipment_list.append(Equipment(**equipment))
    logger.info(f"Equipment in the room {room_id}: {equipment_list}")
    return equipment_list


@app.get("/room/{room_id}")
async def find_room(room_id: int):
    """Достаем обьект room из бд"""

    room = await db.rooms.find_one({"_id": room_id})
    logger.info(f"Room {room_id}: {Room(**room)}")
    return Room(**room)


@app.get("/equipment/{equipment_id}")
async def find_equipment(equipment_id: int):
    """Достаем обьект equipment из бд"""

    equipment = await db.equipment.find_one({"_id": equipment_id})
    logger.info(f"Equipment {equipment_id}: {Equipment(**equipment)}")
    return Equipment(**equipment)


@app.post("/equipment")
async def create_equipment(equipment: Equipment):
    """Добавляем обьект equipment в бд"""

    try:
        await db.equipment.insert_one(equipment.dict(by_alias=True))
        logger.info(f"Equipment with id: {equipment.id}  -  added to the database")
    except:
        logger.warning(f"Equipment with id: {equipment.id}  -  already exists in the database")
    return {"equipment": equipment}


@app.post("/room")
async def create_room(room: Room):
    """Добавляем обьект room в бд"""

    try:
        await db.rooms.insert_one(room.dict(by_alias=True))
        logger.info(f"Room with id: {room.id}  -  added to the database")
    except:
        logger.warning(f"Room with id: {room.id}  -  already exists in the database")
    return {"room": room}


@app.delete("/room/{room_id}")
async def delete_room(room_id: int):
    """Удаляем обьект room из бд"""

    await db.rooms.delete_one({"_id": room_id})
    logger.info(f"Room with id: {room_id}  -  deleted from the database")


@app.delete("/equipment/{equipment_id}")
async def delete_equipment(equipment_id: int):
    """Удаляем обьект equipment из бд"""

    await db.equipment.delete_one({"_id": equipment_id})
    logger.info(f"Equipment with id: {equipment_id}  -  deleted from the database")


@app.put("/room/{room_id}")
async def update_room(room_id: int, new_values_dict: dict):
    """Обновляем/добавляем поле/поля в room в бд"""

    await db.rooms.update_one({"_id": room_id}, {"$set": new_values_dict})
    logger.info(
        f"Room with id: {room_id}  -  updated"
    )  # Если ключа нет в обьекте, то будет добавлена новая пара ключ-значение к этому обьекту


@app.put("/equipment/{equipment_id}")
async def update_equipment(equipment_id: int, new_values_dict: dict):
    """Обновляем/добавляем поле/поля в equipment в бд"""

    await db.equipment.update_one({"_id": equipment_id}, {"$set": new_values_dict})
    logger.info(
        f"Equipment with id: {equipment_id}  -  updated"
    )  # Если ключа нет в обьекте, то будет добавлена новая пара ключ-значение к этому обьекту
