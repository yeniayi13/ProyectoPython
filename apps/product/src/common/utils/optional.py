from typing import TypeVar, Generic

T = TypeVar('T')

class Optional(Generic[T]):
    def __init__(self, value: T = None):
        self.value = value

    def get_value(self):
        if self.has_value():
            return self.value
        raise ValueError("Cannot unwrap an empty Optional")
    
    def has_value(self):
        return self.value is not None

    @staticmethod
    def of(value: T):
        return Optional[T](value)
    
    @staticmethod
    def empty():
        return Optional[T]()