import logging
from typing import AsyncGenerator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from config import get_settings


logger = logging.getLogger(__name__)


class SessionManager:
    def __init__(self):
        settings = get_settings()
        self.async_engine = create_async_engine(url=settings.SQLALCHEMY_URL)
        self.async_session = sessionmaker(
            self.async_engine,
            expire_on_commit=False,
            class_=AsyncSession,
        )

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
        return cls.instance

    def get_session(self) -> AsyncSession:
        return self.async_session()

    def test_connection(self):
        return


async def get_async_session() -> AsyncGenerator:
    async_session = SessionManager().get_session()

    async with async_session:
        try:
            yield async_session
            await async_session.commit()
        except SQLAlchemyError as e:
            await async_session.rollback()
            logger.exception("Get sqlalchemy error")
            raise e
        finally:
            await async_session.close()
