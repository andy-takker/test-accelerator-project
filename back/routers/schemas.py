from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class UserSchema(BaseModel):
    id: Optional[int]
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    age: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class ExtendedUserSchema(UserSchema):

    notifications: List['NotificationSchema']

    class Config:
        orm_mode = True


class UpdateUserSchema(UserSchema):
    username: Optional[str]
    age: Optional[int]


class UserList(BaseModel):
    count: int
    users: List[UserSchema]


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