from src.user.application.repositories.user_repository import User_repository
from src.common.application.application_services import ApplicationService


class Find_client_service(ApplicationService):

    def __init__(
        self,
        user_repo: User_repository
        ):
      super().__init__()
      self.user_repo = user_repo

    async def execute(self, id:str):
        user = await self.user_repo.find_user(id)
        if(user) :
            return user
        
        return {'code':400,'msg':'The user does not exist in the system'}
        
        


