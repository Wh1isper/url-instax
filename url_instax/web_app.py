import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Response

from url_instax.config import get_config
from url_instax.log import logger

from .routers.api.v1 import routers as v1_routers

CURRENT_SERVER_LOCATION = os.environ.get("CURRENT_SERVER_LOCATION", "http://localhost:8890")


@asynccontextmanager
async def lifespan(app: FastAPI):
    config = get_config()
    if config.api_token:
        logger.info("API_TOKEN set, authentication is enabled")
    else:
        logger.info("API_TOKEN not set, authentication is disabled")
    openapi_schema = app.openapi()
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
        }
    }
    openapi_schema["security"] = [{"BearerAuth": []}]

    openapi_schema["servers"] = [
        {"url": CURRENT_SERVER_LOCATION, "description": "Current Server"},
    ]
    app.openapi_schema = openapi_schema
    yield


app = FastAPI(lifespan=lifespan)


@app.middleware("http")
async def verify_token(request, call_next):
    if request.method == "OPTIONS":
        return await call_next(request)

    if request.url.path == "/" or request.url.path == "/docs" or request.url.path == "/openapi.json":
        return await call_next(request)
    config = get_config()
    if not config.api_token:
        # No auth
        return await call_next(request)
    if request.headers.get("Authorization") == f"Bearer {config.api_token}":
        return await call_next(request)

    return Response(
        status_code=401,
        content="Unauthorized. Check environment API_TOKEN for authentication.",
    )


@app.get("/")
async def hello():
    return {"message": "Hello World"}


for router in v1_routers:
    app.include_router(router)
