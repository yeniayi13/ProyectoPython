
from abc import ABC, abstractmethod

from src.orders.application.schemas.product_schemas import Product_in_create


class Product_repository(ABC):
    
    @abstractmethod
    def create_product(product:Product_in_create):
        pass

    @abstractmethod
    def find_product(id:str):
        pass
    
    @abstractmethod
    def product_exists(id:str):
        pass
#
    
    @abstractmethod
    def modify_product(id:str,user):
        pass
    