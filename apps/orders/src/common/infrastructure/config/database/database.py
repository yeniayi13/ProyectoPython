
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import psycopg2

USER='postgres'
PASSWORD='yeniree0813'
HOST='localhost'
PORT='5432'
DATABASE = 'proyectopython'

def create_database():
    conn = psycopg2.connect(
        dbname='postgres',
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT
    )
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DATABASE}'")
    exists = cursor.fetchone()
    if not exists:
        cursor.execute(f"CREATE DATABASE {DATABASE}")
        print(f"Database {DATABASE} created.")
    else:
        print(f"Database {DATABASE} already exists.")

    cursor.close()
    conn.close()

# Verificar y crear la base de datos antes de configurar SQLAlchemy
create_database()

DATABASE_URL = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'

engine = create_engine(DATABASE_URL,
                       echo=True,
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

















