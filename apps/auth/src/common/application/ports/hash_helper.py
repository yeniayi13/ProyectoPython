from abc import ABC,abstractmethod

class Hash_helper(ABC):

    @abstractmethod
    def verify_password(regular_password:str, hashed_password:str)->bool:
        pass
    
    @abstractmethod
    def get_password_hashed(password:str):
        pass