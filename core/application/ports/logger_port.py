from abc import ABC,abstractmethod
class Logger(ABC):
    
    @abstractmethod
    def log_succes():
        pass

    @abstractmethod
    def log_failure():
        pass