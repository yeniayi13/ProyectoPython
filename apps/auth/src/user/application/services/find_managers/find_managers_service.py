from src.user.application.repositories.user_repository import User_repository
from src.common.application.application_services import ApplicationService


class Find_managers_service(ApplicationService):

    def __init__(
        self,
        user_repo: User_repository
        ):
      super().__init__()
      self.user_repo = user_repo

    async def execute(self):
            managers = await self.user_repo.find_managers()
            if (len(managers)==0):
                 return {'code':204,'msg':'There are no managersin the system'}
            
            return managers
        
       
        
        


