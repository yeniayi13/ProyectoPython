from sqlalchemy.ext.asyncio import AsyncSession
from .database import engine, Base
from src.product.infrastructure.models.product_model import ProductModel

# Función asincrónica para crear las tablas
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)