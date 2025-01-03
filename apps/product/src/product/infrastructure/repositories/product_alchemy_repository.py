from datetime import datetime, timezone
from uuid import UUID
from src.product.infrastructure.mappers.map_model_to_product import model_to_product
from src.product.application.schemas.product_schema import Product, ProductCreate, ProductUpdate
from sqlalchemy.future import select
from src.product.infrastructure.models.product_model import ProductModel
from src.product.application.repositories.product_repository import ProductRepository
from src.common.infrastructure.config.database.alchemy_base_repository import BaseRepository
from src.common.utils.optional import Optional

class ProductAlchemyRepository(BaseRepository, ProductRepository):

    def __init__(self, db):
        super().__init__(db)

    async def get_all(self) -> list[Product]:
        result = await self.db.execute(select(ProductModel))
        products = result.scalars().all()
        return [model_to_product(product) for product in products]

    async def get_by_id(self, id: UUID) -> Optional[Product]:
        result = await self.db.execute(select(ProductModel).where(ProductModel.id == id))
        product = result.scalar_one_or_none()
        if product is None:
            return Optional.empty()
        else:
            return Optional.of(model_to_product(product))

    async def create(self, product_data: ProductCreate) -> Product:
        try:
            print(f"Creando producto con los siguientes datos: {product_data.dict()}")
            new_product = ProductModel(**product_data.dict())
            self.db.add(new_product)
            await self.db.commit()
            await self.db.refresh(new_product)
            return model_to_product(new_product)
        except Exception as e:
            await self.db.rollback()
            raise

    async def update(self, product_data: ProductUpdate) -> Product:
        try:
            # Obtener el producto existente
            product_model = (
                await self.db.execute(select(ProductModel).where(ProductModel.id == product_data.id))
            ).scalar_one_or_none()
            
            if product_model is None:
                raise ValueError(f"Product with id {product_data.id} not found")
            # Convertir product_data a un diccionario, filtrando valores None
            update_dict = {
                k: v for k, v in product_data.dict(exclude_unset=True).items()
                if v is not None and k != 'id'
            }

            # Recalcular el precio si cost o margin están presentes
            if 'cost' in update_dict or 'margin' in update_dict:
                cost = update_dict.get('cost', product_model.cost)
                margin = update_dict.get('margin', product_model.margin)
                if margin >= 1:
                    raise ValueError("El margen debe ser menor que 1 para calcular el precio")
                update_dict['price'] = round(cost / (1 - margin), 2)

            print(f"Actualizando producto con los siguientes datos: {update_dict}")
            # Actualizar los atributos del modelo
            for key, value in update_dict.items():
                setattr(product_model, key, value)
            # Actualizar la marca de tiempo de updated_at
            product_model.updated_at = datetime.now(timezone.utc)
            await self.db.commit()
            await self.db.refresh(product_model)
            #print(f"Producto actualizado en la base de datos: {product_model.__dict__}")
            #print(f"Valores del esquema ProductResponse: {model_to_product(product_model).dict()}")
            return model_to_product(product_model)
        except Exception as e:
            print('rolling back')
            await self.db.rollback()
            raise

    async def delete(self, product_id: UUID) -> None:
        try:
            product_model = (
                await self.db.execute(select(ProductModel).where(ProductModel.id == product_id))
            ).scalar_one_or_none()
            if product_model is not None:
                await self.db.delete(product_model)
                await self.db.commit()
            else: raise ValueError(f"Product with id {product_id} not found")
        except Exception as e:
            await self.db.rollback()
            raise
