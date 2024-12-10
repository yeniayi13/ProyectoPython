

# Not Ready

from core.application.application_services import ApplicationService

class AuditingDecorator[TService,TRespond](ApplicationService):

    decoratee: ApplicationService

    def __init__(self, decoratee):
        pass

    def execute(TService) -> TRespond:
        pass