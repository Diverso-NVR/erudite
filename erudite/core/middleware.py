import logging
from contextlib import asynccontextmanager

from fastapi import Request, Response
from fastapi.responses import JSONResponse
import asyncpg

from .settings import settings

PSQL_DATABASE_ADRESS: str = settings.psql_url

logger = logging.getLogger("erudite")


@asynccontextmanager
async def db_connect():
    conn = await asyncpg.connect(PSQL_DATABASE_ADRESS)
    try:
        yield conn
    finally:
        await conn.close()


async def authorization(request: Request, call_next):
    if (
        request.url.path
        in [
            "/api/erudite/docs",
            "/api/erudite/redoc",
            "/api/erudite/openapi.json",
        ]
        or request.method == "GET"
    ):
        return await call_next(request)

    api_key = request.headers.get("key")
    if api_key is None:
        return JSONResponse(status_code=401, content={"message": "No API key provided"})

    response = await check_key(api_key)
    if not response.status_code == 200:
        return response

    return await call_next(request)


async def check_key(key: str):
    async with db_connect() as conn:
        user = await conn.fetchrow("SELECT * FROM users WHERE api_key = $1", key)

    if not user:
        return JSONResponse(status_code=401, content={"message": "Invalid API key"})

    return Response(status_code=200)
