from utils.errors import Error

class Result[T]:
    value:T
    error: Error
    is_failure: bool
    
    def __init__(self, value: T | None, error: Error | None) -> Result[T]:
        if (value is None) and (error is None):
            raise ValueError("The result must recibe one input, this has both attributes as None")
        if (value is not None) and (error is not None):
            raise ValueError("The result must recibe JUST ONE input, this has both attributes value, and error with values ")
        
        self.is_failure = self.error is not None
        self.error = error
        self.value = value

    def get_error_message(self) -> str:
        if (self.error is None):
            raise 'There is no Error message, this may be OK'    
        return self.__str__()
    

    def result(self) -> T:
        if(self.value is None):
            raise ValueError("There is no value, this may be an error")
        return self.value

    def is_succes(self) -> bool: 
        return self.value is not None

    def is_error(self) -> bool : 
        return self.error is not None
    
    
    
    @staticmethod
    def success(value: T):
        return Result(value=value, error=None)
    
    @staticmethod
    def failure(error: Error):
        return Result(value=None, error=error)    