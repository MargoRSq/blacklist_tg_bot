from sqlalchemy.orm import relationship
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


class Blacklist(Base):
    __tablename__ = 'blacklist_table'

    id = Column(Integer, primary_key=True)
    url = Column(String(100))
    added_by = Column(Enum(UserType))
    chat_id = Column(BigInteger)
    message_id = Column(BigInteger)
    chat_type = Column(Enum(ChatType))


class Users(Base):
    __tablename__ = 'users_table'

    id = Column(Integer, primary_key=True)
    role = Column(Enum(UserType))
    url = Column(String(100))

# new_user = Blacklist(id=123, url="@lol", added_by=UserType.superadmin,
# 					 chat_id=-11231, message_id=2)


# stmt = (
#     insert(Blacklist).
#     values(new_user.id, new_user.url, new_user.added_by,
#            new_user.chat_id, new_user.message_id)
# )b


Base.metadata.create_all(engine)

# print(stmt)

# with engine.connect() as conn:
#     result = conn.execute(stmt)
