from abc import ABC,abstractmethod
class Identifier(ABC):
    
    @abstractmethod
    def create_id() -> str:
        pass
    