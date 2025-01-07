from src.cart.application.schemas.cart_schemas import Cart_in_delete, Cart_in_modify
from abc import ABC, abstractmethod

from src.common.utils.result import Result


class Cart_repository(ABC):
    
    @abstractmethod
    def add_product_to_cart():
        pass

    @abstractmethod
    def product_already_in_cart(id:str):
        pass

    @abstractmethod
    def modify_quantity_in_cart(cart:Cart_in_modify):
        pass
    
    @abstractmethod
    def remove_product_from_cart(product:Cart_in_delete)->Result:
        pass
        
    @abstractmethod 
    def get_cart(client_id):
        pass