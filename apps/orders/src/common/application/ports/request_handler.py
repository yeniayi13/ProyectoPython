from abc import ABC,abstractmethod

class Request_handler(ABC):
    
    @abstractmethod
    def discount_product_quantity(route: str,product_id: str, quantity: int ) -> str:
        pass
    
    @abstractmethod
    def replenish_cancelled_products(route: str,products:dict) -> str:
        pass
    
    

    #@abstractmethod
    #def put() -> str:
    #    pass
    #
    #@abstractmethod
    #def delete() -> str:
    #    pass
#
    #@abstractmethod
    #def patch() -> str:
    #    pass
    
    
    