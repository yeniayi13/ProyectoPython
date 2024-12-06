from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

USER=''
PASSWORD=''
HOST='localhost'
PORT='5432'
DATABASE = 'postgres'

DATABASE_URL = f'postgres://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'

engine = create_engine(DATABASE_URL)

session_local = sessionmaker(autoflush=False, autocommit = False, bind = engine)

Base = declarative_base()

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close() 