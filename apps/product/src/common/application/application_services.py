from abc import ABC, abstractmethod
from typing import TypeVar

TService = TypeVar('TService')
TRespond = TypeVar('TRespond')

class ApplicationService[TService, TRespond](ABC):
    @abstractmethod
    def execute(self, data: TService) -> TRespond:
        pass