from sqlalchemy.orm import as_declarative
from sqlalchemy import Column, Integer


@as_declarative()
class Base:
    id = Column(Integer, primary_key=True, index=True)
