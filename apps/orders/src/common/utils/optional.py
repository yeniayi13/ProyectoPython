class Optional[T]:
    def __init__(self, value = None):
        self.value = value
        pass

    def unwrap(self):
        if self.has_value():
            return self.value
        raise "It can't be unwrapped, is empty"

    def has_value(self):
        return self.has_value is not None

    @staticmethod
    def full[T](value:T):
        return Optional(value)
    
    @staticmethod
    def empty[T]():
        return Optional()