
from fastapi import FastAPI

from routers.user_router import user_router

def create_app() -> FastAPI:
    app = FastAPI(
        title='Тестовое приложение',
        version='0.0.1a',
    )

    app.include_router(user_router)

    return app


app = create_app()