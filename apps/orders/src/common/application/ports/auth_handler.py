
from abc import ABC,abstractmethod


class Auth_handler(ABC):
    

    @abstractmethod
    def sign(id:str ,role:str)-> str :
        pass


    @abstractmethod
    def decode(token:str):
        pass
