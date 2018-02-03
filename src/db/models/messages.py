from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date
from sqlalchemy.orm import relationship
import enum

from .Base import Base

class MessageThread(Base):
    __tablename__ = 'message_threads'

    id = Column(Integer, unique=True)
    user_id = Column(String, ForeignKey('users.id'), primary_key=True)
    person = Column(String, primary_key=True)
    messages = relationship('Message')

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    thread_id = Column(Integer, ForeignKey('message_threads.id'))
    type = Column(String)
    body = Column(String)
    date = Column(Date)
    user_speaking = Column(Boolean)
