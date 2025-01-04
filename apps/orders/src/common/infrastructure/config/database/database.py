from src.common.infrastructure.config.config import get_settings
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import psycopg2


stgs = get_settings()


def create_database():
    conn = psycopg2.connect(
        dbname= stgs.DATABASE,
        user= stgs.POSTGRES_USER,   
        password= stgs.PASSWORD,    
        host= stgs.HOST,  
        port= stgs.PORT  
    )
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{stgs.DATABASE}'")
    exists = cursor.fetchone()
    if not exists:
        cursor.execute(f"CREATE DATABASE {stgs.DATABASE}")
        print(f"Database {stgs.DATABASE} created.")
    else:
        print(f"Database {stgs.DATABASE} already exists.")

    cursor.close()
    conn.close()

# Verificar y crear la base de datos antes de configurar SQLAlchemy
create_database()

#DATABASE_URL = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'
DATABASE_URL = f'postgresql://{stgs.POSTGRES_USER}:{stgs.PASSWORD}@{stgs.HOST}:{stgs.PORT}/{stgs.DATABASE}'
engine = create_engine(DATABASE_URL,
                       echo=False,
                       pool_size=5,
                       max_overflow=10,
                       pool_timeout=30,
                       pool_recycle=1800)

session_local = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

















