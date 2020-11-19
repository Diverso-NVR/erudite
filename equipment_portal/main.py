from fastapi import FastAPI
import motor.motor_asyncio
import logging

from db.models import Equipment, Room, db
from routes import rooms, equipment

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

app.include_router(rooms.router)
app.include_router(equipment.router)