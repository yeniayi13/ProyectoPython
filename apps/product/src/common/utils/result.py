from typing import TypeVar, Generic
from src.common.utils.errors import Error

T = TypeVar('T')

class NoValue:
    pass

# Instancia única para usar como marcador
NO_VALUE = NoValue()

class Result(Generic[T]):
    value: T | NoValue
    error: Error | None
    is_failure: bool

    def __init__(self, value: T | NoValue = NO_VALUE, error: Error | None = None):
        # Validar que al menos uno de los parámetros sea válido
        if value is NO_VALUE and error is None:
            raise ValueError("The result must receive one input; both attributes are None")
        
        if value is not NO_VALUE and error is not None:
            raise ValueError("The result must receive JUST ONE input; both value and error have values")
        
        # Asignar los valores
        self.value = value if value is not NO_VALUE else None
        self.error = error
        self.is_failure = error is not None

    def get_error_message(self) -> str:
        if self.error is None:
            raise ValueError("There is no error message; this may be OK")
        return self.error.msg

    def get_data(self) -> T:
        if self.value is NO_VALUE:
            raise ValueError("There is no value; this may be an error")
        return self.value

    def is_success(self) -> bool:
        return self.is_failure is False

    def is_error(self) -> bool:
        return self.is_failure is True

    @staticmethod
    def success(value: T):
        return Result(value=value, error=None)

    @staticmethod
    def failure(error: Error):
        return Result(value=NO_VALUE, error=error)