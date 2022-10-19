
import random

from fastapi import FastAPI
from fastapi_pagination import add_pagination

from config import get_settings
from middlewares import RedisMiddleware
from routers.user_router import user_router

def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title='Тестовое приложение',
        version='0.0.1a',
    )

    app.include_router(user_router)
    app.add_middleware(
        RedisMiddleware,
        settings=settings,
    )
    add_pagination(app)
    return app
