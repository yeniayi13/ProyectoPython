from abc import ABC,abstractmethod



class Event_handler(ABC):
    
    @abstractmethod
    def publish(event:dict, key, exchange):
        pass
    
    @abstractmethod
    def consume():
        pass



