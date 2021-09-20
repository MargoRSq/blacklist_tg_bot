import enum

from sqlalchemy import Column, Integer, String, Enum, BigInteger

from db.db import engine, Base


class UserType(enum.Enum):
    user = 'user'
    admin = 'admin'
    superadmin = 'superadmin'


class ChatType(enum.Enum):
    channel = 'channel'
    group = 'group'
    private = 'private'

class State(enum.Enum):
    waiting4add = 1
    waiting4request = 2
    waiting4add = 3
    waiting4remove = 4
    waiting4mailing = 5
    waiting4add_admin = 6


class StateSaver(Base):
    __tablename__ = 'state_table'

    id = Column(Integer, primary_key=True)
    state = Column(Enum(State))


class Blacklist(Base):
    __tablename__ = 'blacklist_table'

    id = Column(Integer, primary_key=True)
    url = Column(String(100))
    added_by = Column(Enum(UserType))
    chat_id = Column(BigInteger)
    message_id = Column(BigInteger)
    chat_type = Column(Enum(ChatType))
    chat_name = Column(String(100))


class Users(Base):
    __tablename__ = 'users_table'

    id = Column(Integer, primary_key=True)
    role = Column(Enum(UserType))
    url = Column(String(100))


