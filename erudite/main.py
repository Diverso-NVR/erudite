import logging
from starlette.middleware.base import BaseHTTPMiddleware


# функция логгера
def create_logger(mode="INFO"):
    logs = {"INFO": logging.INFO, "DEBUG": logging.DEBUG}

    logger = logging.getLogger("erudite")
    logger.setLevel(logs[mode])

    handler = logging.StreamHandler()
    handler.setLevel(logs[mode])

    formatter = logging.Formatter("%(levelname)-8s  %(asctime)s    %(message)s", datefmt="%d-%m-%Y %I:%M:%S %p")

    handler.setFormatter(formatter)

    logger.addHandler(handler)


def create_app():
    create_logger()  # Создание логгера

    from fastapi import FastAPI

    app = FastAPI()

    from routers.rooms import router as room_router
    from routers.equipment import router as equipment_router

    app.include_router(room_router)
    app.include_router(equipment_router)

    from middleware import authorization

    app.add_middleware(BaseHTTPMiddleware, dispatch=authorization)  # применяется ко всем запросам

    return app


app = create_app()
