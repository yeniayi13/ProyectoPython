from abc import ABC,abstractmethod

class ApplicationService[TService,TRespond](ABC):
    
    @abstractmethod
    def execute(self,service: TService)->TRespond:
        pass