from starlette.middleware.base import BaseHTTPMiddleware

from fastapi.openapi.utils import get_openapi

from core.settings import create_logger


def create_app():
    create_logger("erudite")  # Создание логгера

    from fastapi import FastAPI

    app = FastAPI(root_path="/api/erudite")

    from core.routers.rooms import router as room_router
    from core.routers.equipment import router as equipment_router
    from core.routers.disciplines import router as discipline_router

    app.include_router(room_router)
    app.include_router(equipment_router)
    app.include_router(discipline_router)

    from core.middleware import authorization

    app.add_middleware(BaseHTTPMiddleware, dispatch=authorization)

    return app


app = create_app()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Erudite",
        version="1.0.0",
        description="Erudite – db of rooms, equipment, disciplines and stuff in MIEM. Kinda Google AdminSDK",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {"url": "https://avatars2.githubusercontent.com/u/64712541"}

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=6000)
