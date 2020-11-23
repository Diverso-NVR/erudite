from starlette.middleware.base import BaseHTTPMiddleware
from core.settings import create_logger


def create_app():
    create_logger("erudite")  # Создание логгера

    from fastapi import FastAPI

    app = FastAPI()

    from core.routers.rooms import router as room_router
    from core.routers.equipment import router as equipment_router

    app.include_router(room_router)
    app.include_router(equipment_router)

    from core.middleware import authorization

    app.add_middleware(
        BaseHTTPMiddleware, dispatch=authorization
    )  # применяется ко всем запросам

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=6000)
