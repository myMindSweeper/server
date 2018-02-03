from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
import enum

from .Base import Base

class MessageThread(Base):
    __tablename__ = 'message_threads'

    id = Column(Integer, unique=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    person = Column(String, primary_key=True)
    messages = relationship('Message')

class MessageType(enum.Enum):
    SMS = 1

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    thread_id = Column(Integer, ForeignKey('message_threads.id'))
    type = Column(Enum(MessageType))
    body = Column(String)
    user_speaking = Column(Boolean)
