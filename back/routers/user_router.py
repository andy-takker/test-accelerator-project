from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response
from fastapi_pagination import LimitOffsetPage, LimitOffsetParams
from fastapi_pagination.ext.async_sqlalchemy import paginate
from pydantic import parse_obj_as
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from sqlalchemy.orm import selectinload

from db import User, Notification
from db.engine import get_async_session
from error_handlers import ErrorMessage, UniqueObjectException
from jobs import create_user_job
from routers.schemas import (
    NotificationList,
    NotificationSchema,
    UpdateUserSchema,
    UserSchema,
    ExtendedUserSchema,
    OutputUserSchema,
)

user_router = APIRouter(prefix="/users", tags=["Пользователи"])


@user_router.get(
    path="/",
    name="Все пользователи",
    response_model=LimitOffsetPage[OutputUserSchema],
)
async def get_all_users(
    limit: int = Query(lt=100, gt=0, default=50),
    offset: int = Query(gt=-1, default=0),
    session: AsyncSession = Depends(get_async_session),
):
    q = select(User)
    return await paginate(
        session, q, params=LimitOffsetParams(limit=limit, offset=offset)
    )


@user_router.post(
    path="/",
    name="Добавить пользователя",
    response_model=OutputUserSchema,
    responses={
        400: {
            "model": ErrorMessage,
            "description": "Some problem with input data",
            "content": {
                "application/json": {"example": {"message": "Username is not unique!"}}
            },
        }
    },
)
async def create_user(
    user: UserSchema, session: AsyncSession = Depends(get_async_session)
):
    q = select(User).where(User.username == user.username)
    old_user = (await session.execute(q)).scalars().first()
    if old_user is not None:
        raise UniqueObjectException(fieldname="username")
    u = User()
    d = user.dict()
    for k in d:
        setattr(u, k, d[k])
    session.add(u)
    await session.commit()
    await session.refresh(u)
    return UserSchema.from_orm(u)


@user_router.get(
    "/{user_id}", name="Получить пользователя", response_model=ExtendedUserSchema
)
async def get_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    user = await session.get(User, user_id, options=[selectinload(User.notifications)])
    if user is not None:
        return ExtendedUserSchema.from_orm(user)
    raise HTTPException(status_code=404, detail="User not found!")


@user_router.delete("/{user_id}", name="Удалить пользователя", response_class=Response)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    q = delete(User).where(User.id == user_id)
    await session.execute(q)
    return Response(status_code=204)


@user_router.put(
    "/{user_id}", name="Обновить данные пользователя", response_model=UserSchema
)
async def update_user(
    user_id: int,
    new_user_data: UpdateUserSchema,
    session: AsyncSession = Depends(get_async_session),
):
    u = await session.get(User, user_id)
    if u is not None:
        data = new_user_data.dict()
        for key in data:
            if data[key] is not None:
                setattr(u, key, data[key])
        session.add(u)
        await session.commit()
        await session.refresh(u)
        return UserSchema.from_orm(u)
    raise HTTPException(status_code=404, detail="User not found!")


@user_router.get("/{user_id}/notifications", tags=["Уведомления"])
async def get_user_notifications(
    user_id: int, session: AsyncSession = Depends(get_async_session)
):
    u = await session.get(User, user_id)
    if u is None:
        raise HTTPException(status_code=404, detail="User not found!")

    q = select(Notification).where(Notification.user_id == user_id)

    notifications = (await session.execute(q)).scalars().all()
    return NotificationList(
        count=len(notifications),
        notifications=parse_obj_as(List[NotificationSchema], notifications),
    )


@user_router.post("/create-background-task", tags=["Фоновые задачи"])
async def create_background_task(
    request: Request,
    age: int = Query(),
    username: str = Query(),
):
    request.state.queue.enqueue(create_user_job, username, age)
    return {
        "success": True,
    }
