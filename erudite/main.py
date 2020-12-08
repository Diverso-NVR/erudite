from starlette.middleware.base import BaseHTTPMiddleware

from fastapi.openapi.utils import get_openapi

from core.settings import create_logger


def create_app():
    create_logger("erudite")  # Создание логгера

    from fastapi import FastAPI

    # app = FastAPI(root_path="/api/erudite")
    app = FastAPI()

    from core.routes.rooms import router as room_router
    from core.routes.equipment import router as equipment_router
    from core.routes.disciplines import router as discipline_router

    app.include_router(room_router)
    app.include_router(equipment_router)
    app.include_router(discipline_router)

    # DEVELOPER change in prod
    # from core.middleware import authorization

    # app.add_middleware(BaseHTTPMiddleware, dispatch=authorization)

    return app


app = create_app()


@app.get("/", tags=["Root"], summary="Root", description="Welcome to Erudite!")
async def read_root():
    return {"message": "Welcome to Erudite!"}


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
