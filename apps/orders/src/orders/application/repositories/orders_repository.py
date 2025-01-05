
from abc import ABC, abstractmethod

from src.orders.application.schemas.order_schemas import Product_in_order


class Order_repository(ABC):
    @abstractmethod
    def create_order(client_id:str, products: list[Product_in_order]):
        pass

    @abstractmethod
    def find_order(id:str):
        pass
    
    @abstractmethod
    def order_exists(email:str):
        pass

    
    @abstractmethod
    def cancel_order(order_id:str,user):
        pass

    @abstractmethod
    def get_order(order_id:str):
        pass

    @abstractmethod
    def find_orders(client_id:str):
        pass