
from abc import ABC, abstractmethod


class Client_repository(ABC):
    @abstractmethod
    def create_client():
        pass

    @abstractmethod
    def find_client(id:str):
        pass
    
    @abstractmethod
    def client_exists(email:str):
        pass

    
    @abstractmethod
    def modify_client(id:str, client_in_modify):
        pass
    