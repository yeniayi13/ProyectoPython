from core.utils.result import Result
from core.application.application_services import ApplicationService
from core.application.ports.logger_port import Logger

class LoggingDecorator[TService,TRespond](ApplicationService):

    decoratee: ApplicationService 
    def __init__(self, decoratee:ApplicationService, logger:Logger):
        self.logger = logger
        self.decoratee = decoratee

    async def execute(self,service):
        result:Result= await self.decoratee.execute(service)

        if(result.is_error()):
            error = f" service: {type(self.decoratee)} has failed: {result.get_error_message()}"
            self.logger.log_failure(error)
            return result.get_error_message()
        if (result.is_succes()):
            info = f" service: {type(self.decoratee)} with {str(service)} body has been succesfull"
            self.logger.log_succes(info)
            return result.develop()