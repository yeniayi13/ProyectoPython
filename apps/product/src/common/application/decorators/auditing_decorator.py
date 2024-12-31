from typing import TypeVar
from src.common.application.application_services import ApplicationService

TService = TypeVar('TService')
TRespond = TypeVar('TRespond')

class AuditingDecorator[TService,TRespond](ApplicationService[TService,TRespond]):

    decoratee: ApplicationService

    def __init__(self, decoratee):
        pass

    def execute(self, data: TService) -> TRespond:
        pass