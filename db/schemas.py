from sqlalchemy.orm import relationship
import enum

from sqlalchemy import Table, Column, Integer, String, Enum, insert, select

from sqlalchemy.sql.functions import user
from sqlalchemy.orm import declarative_base, session

from db.db import engine, Base, metadata_obj, session


class UserType(enum.Enum):
    user = 'user'
    admin = 'admin'
    superadmin = 'superadmin'


class Blacklist(Base):
    __tablename__ = 'blacklist_table'

    id = Column(Integer, primary_key=True)
    url = Column(String(100))
    added_by = Column(Enum(UserType))
    chat_id = Column(Integer)
    message_id = Column(Integer)

    def __repr__(self):
        return f"User(id={self.id!r}, url={self.url!r}, chat_id={self.chat_id!r})"


new_user = Blacklist(id=123, url="@lol", added_by=UserType.superadmin,
                     chat_id=-11231, message_id=2)


# stmt = (
#     insert(Blacklist).
#     values(new_user.id, new_user.url, new_user.added_by,
#            new_user.chat_id, new_user.message_id)
# )b


# Base.metadata.create_all(engine)

# print(stmt)

# with engine.connect() as conn:
#     result = conn.execute(stmt)
