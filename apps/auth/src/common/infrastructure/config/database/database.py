from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.common.infrastructure.config.config import get_settings

settings = get_settings()

USER = settings.POSTGRES_USER
PASSWORD = settings.PASSWORD
HOST = settings.HOST
PORT = settings.PORT
DATABASE = settings.DATABASE


DATABASE_URL = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'
engine = create_engine(DATABASE_URL,
                       echo=False,
                       pool_size=5,     
                       max_overflow=10,
                       pool_timeout=30,
                       pool_recycle=1800)

session_local = sessionmaker(autoflush=False, autocommit = False, bind = engine)

Base = declarative_base()

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close() 