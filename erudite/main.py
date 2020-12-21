from starlette.middleware.base import BaseHTTPMiddleware

from fastapi.openapi.utils import get_openapi

from core.settings import create_logger, settings


def create_app():
    create_logger("erudite")  # Logger creation

    from fastapi import FastAPI

    if settings.dev:
        app = FastAPI()
    else:
        app = FastAPI(root_path="/api/erudite")
        from core.middleware import authorization

        app.add_middleware(BaseHTTPMiddleware, dispatch=authorization)

    from core.routes.rooms import router as room_router
    from core.routes.equipment import router as equipment_router
    from core.routes.disciplines import router as discipline_router
    from core.routes.lessons import router as lesson_router

    app.include_router(room_router)
    app.include_router(equipment_router)
    app.include_router(discipline_router)
    app.include_router(lesson_router)

    return app


app = create_app()


@app.get("/", include_in_schema=False)
async def read_root():
    return {"message": "Welcome to Erudite!"}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Erudite",
        version="1.0.2",
        description=(
            "Erudite – db of rooms, equipment, disciplines and stuff in MIEM. Kinda Google AdminSDK"
        ),
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://avatars2.githubusercontent.com/u/64712541"
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=6000)
