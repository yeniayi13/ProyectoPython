from abc import ABC, abstractmethod
from uuid import UUID
from src.common.utils.optional import Optional
from src.product.application.schemas.product_schema import ProductCreate, ProductUpdate
from src.product.application.schemas.product_schema import Product

class ProductRepository(ABC):
    @abstractmethod
    def get_all() -> list[Product]:
        pass
    
    @abstractmethod
    def get_by_id(id: UUID) -> Optional[Product]:
        pass
    
    @abstractmethod 
    def create(product: ProductCreate) -> Product:
        pass
    
    @abstractmethod
    def update(product: ProductUpdate) -> Product:
        pass
    
    @abstractmethod
    def delete(id: UUID) -> None:
        pass