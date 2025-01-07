from abc import ABC, abstractmethod
from typing import Generic, TypeVar

TService = TypeVar('TService')
TRespond = TypeVar('TRespond')

class ApplicationService(ABC, Generic[TService, TRespond]):
    @abstractmethod
    def execute(self, data: TService) -> TRespond:
        pass