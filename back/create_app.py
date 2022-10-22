from fastapi import FastAPI
from fastapi_pagination import add_pagination

from config import get_settings
from error_handlers import unique_validation_handler, UniqueObjectException
from middlewares import RedisMiddleware
from routers.user_router import user_router
from routers.ping_router import ping_router


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="Тестовое приложение",
        version="0.0.1a",
        debug=False,
    )

    app.include_router(user_router)
    app.include_router(ping_router)
    app.add_middleware(
        RedisMiddleware,
        settings=settings,
    )
    app.add_exception_handler(UniqueObjectException, unique_validation_handler)
    add_pagination(app)
    return app
