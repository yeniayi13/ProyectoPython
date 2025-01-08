from abc import ABC,abstractmethod

class Request_handler(ABC):
    
    @abstractmethod
    def get() -> str:
        pass
    
    @abstractmethod
    def post() -> str:
        pass

    @abstractmethod
    def put() -> str:
        pass
    
    @abstractmethod
    def delete() -> str:
        pass

    @abstractmethod
    def patch() -> str:
        pass
    
    
    