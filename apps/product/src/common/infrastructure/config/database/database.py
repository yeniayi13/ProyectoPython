from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from src.common.infrastructure.config.config import get_settings

settings = get_settings()

USER =settings.POSTGRES_USER    #user
PASSWORD =settings.POSTGRES_PASSWORD    #secret
HOST =settings.POSTGRES_HOST    #localhost
PORT =settings.POSTGRES_PORT   #5434
DATABASE =settings.POSTGRES_DATABASE    #product

DATABASE_URL = f'postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'

engine = create_async_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker( bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def get_db():
    async with SessionLocal() as session:
        yield session
