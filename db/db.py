from sqlalchemy import text
import sqlalchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, session, sessionmaker
from sqlalchemy import MetaData
from sqlalchemy.sql.selectable import Select
from utils.config import DATABASE_URL


engine = create_engine(DATABASE_URL, echo=False)

Base = declarative_base()
metadata_obj = MetaData()

Session = sessionmaker(bind=engine)

session = Session()
