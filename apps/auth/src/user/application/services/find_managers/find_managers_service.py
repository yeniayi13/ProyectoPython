from src.user.application.schemas.user_schermas import User_in_response
from src.common.utils.result import Result
from src.user.application.repositories.user_repository import User_repository
from src.common.application.application_services import ApplicationService
from src.common.utils.errors import Error

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
                 return Result.failure(Error('NoManagers', 'There are no managers in the system',404))
            
            managers_result=[]
            
            for manager in managers:
                 user_response = User_in_response(id= manager.id, 
                            name= f'{manager.first_name} {manager.last_name}',
                            username= manager.username,
                            c_i= manager.c_i, email= manager.email
                            )
                 managers_result.append(user_response)
                 
                 
            return Result.success(managers_result)
        
       
        
        


