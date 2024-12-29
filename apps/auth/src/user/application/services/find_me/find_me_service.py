from src.common.utils.result import Result
from src.user.application.schemas.user_schermas import User_in_response
from src.user.application.repositories.user_repository import User_repository
from src.common.application.application_services import ApplicationService
from src.common.utils.errors import Error

class Find_me_service(ApplicationService):

    def __init__(
        self,
        user_repo: User_repository
        ):
      super().__init__()
      self.user_repo = user_repo

    async def execute(self, user_id:str):
        user = await self.user_repo.find_user(user_id)
        if(user) :
            response = User_in_response(id= user.id, 
                            name= f'{user.first_name} {user.last_name}',
                            username= user.username,
                            c_i= user.c_i, email= user.email
                            )
            
            return Result.success(response)
        
        return Result.failure(Error('UserNotFound', 'The user does not exist in the system', 404))
        
        


