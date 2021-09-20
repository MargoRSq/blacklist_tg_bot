from sqlalchemy import text
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import MetaData
from utils.config import DATABASE_URL


engine = create_engine(DATABASE_URL, echo=False)

Base = declarative_base()
metadata_obj = MetaData()

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

session = Session()
