from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    id: int | None = Field(title="User ID")
    username: str = Field(title="Unique username")
    first_name: str | None
    last_name: str | None
    age: int

    class Config:
        orm_mode = True


class OutputUserSchema(UserSchema):
    created_at: datetime | None
    updated_at: datetime | None


class ExtendedUserSchema(OutputUserSchema):

    notifications: List["NotificationSchema"]

    class Config:
        orm_mode = True


class UpdateUserSchema(UserSchema):
    username: Optional[str]
    age: Optional[int]


class NotificationSchema(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    message: str

    class Config:
        orm_mode = True


class NotificationList(BaseModel):
    count: int
    notifications: List[NotificationSchema]


ExtendedUserSchema.update_forward_refs()
