from abc import ABC, abstractmethod


class Cart_repository(ABC):
    
    @abstractmethod
    def add_product_to_cart():
        pass

    @abstractmethod
    def product_already_in_cart(id:str):
        pass
    