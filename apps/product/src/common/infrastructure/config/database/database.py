from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.common.infrastructure.config.config import get_settings

settings = get_settings()

USER = settings.POSTGRES_USER
PASSWORD = settings.POSTGRES_PASSWORD
HOST = settings.POSTGRES_HOST
PORT = settings.POSTGRES_PORT
DATABASE = settings.POSTGRES_DATABASE

DATABASE_URL = f'postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def get_db():
    async with SessionLocal() as session:
        yield session
