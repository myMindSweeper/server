from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from .Base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True)
    threads = relationship('MessageThread')
