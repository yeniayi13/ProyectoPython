
from abc import ABC, abstractmethod


class User_repository(ABC):
    @abstractmethod
    def create_user():
        pass

    @abstractmethod
    def find_user(id:str):
        pass
    
    @abstractmethod
    def user_exists(email:str):
        pass

    @abstractmethod
    def create_manager(user):
        pass