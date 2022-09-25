from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel
from pydantic.dataclasses import dataclass


@dataclass
class User:
    id: int
    username: str
    first_name: str
    last_name: str
    age: int
    created_at: datetime

class UpdateUserSchema(BaseModel):
    id: Optional[int] 
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    age: Optional[int]
    created_at: Optional[datetime]



@dataclass
class UserList:
    count: int
    users: List[User]
