from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

USER='user'
PASSWORD='password'
HOST='localhost'
PORT='5432'
DATABASE = 'postgres'

DATABASE_URL = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'

engine = create_engine(DATABASE_URL,
                       echo=True,
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