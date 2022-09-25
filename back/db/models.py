from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship
from db.base import Base
from db.mixins import TimestampMixin


class User(TimestampMixin, Base):
    __tablename__ = 'user'

    
    username = Column(String(128), index=True, nullable=False)
    first_name = Column(String(64) )
    last_name = Column(String(64))
    age = Column(Integer, nullable=False)

    notifications = relationship('Notification', back_populates='user')


class Notification(TimestampMixin, Base):
    __tablename__ = 'notification'

    user_id = Column(ForeignKey('user.id'), index=True, nullable=False)
    message = Column(String(512), nullable=False, default='')

    user = relationship('User', back_populates='notifications')

