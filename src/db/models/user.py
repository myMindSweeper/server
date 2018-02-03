from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from .Base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    threads = relationship('MessageThread')
