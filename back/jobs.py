import asyncio
import logging
import time

from db.engine import SessionManager
from db import User

logger = logging.getLogger(__name__)


async def _create_user(username: str, age: int):
    async_session = SessionManager().get_session()

    async with async_session:
        try:
            user = User(username=username, age=age)
            async_session.add(user)
            await async_session.commit()
        except SQLAlchemyError as exc:
            await async_session.rollback()
            logger.error('Get sqlalchemy error')
            raise exc
        finally:
            await async_session.close()


def create_user_job(username: str, age: int):
    asyncio.run(_create_user(username, age))