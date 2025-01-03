
from abc import ABC, abstractmethod


class Product_repository(ABC):
    
    @abstractmethod
    def create_product():
        pass

    #@abstractmethod
    #def find_product(id:str):
    #    pass
    #
    #@abstractmethod
    #def product_exists(email:str):
    #    pass
#
    #
    #@abstractmethod
    #def modify_product(id:str,user):
    #    pass
    