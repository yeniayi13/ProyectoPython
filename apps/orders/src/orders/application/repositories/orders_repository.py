
from abc import ABC, abstractmethod


class Order_repository(ABC):
    @abstractmethod
    def create_order():
        pass

    @abstractmethod
    def find_order(id:str):
        pass
    
    @abstractmethod
    def order_exists(email:str):
        pass

    
    @abstractmethod
    def modify_order(id:str,user):
        pass
    