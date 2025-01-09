from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.common.infrastructure.config.config import get_settings_auth

stgs = get_settings_auth()

DATABASE_URL = f'postgresql://{stgs.POSTGRES_USER}:{stgs.PASSWORD}@{stgs.HOST}:{stgs.PORT}/{stgs.DATABASE}'
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