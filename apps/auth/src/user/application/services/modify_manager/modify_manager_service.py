from datetime import datetime
from src.user.application.services.modify_manager.types.modify_manager_dto import Modify_manager_dto
from src.user.application.schemas.user_schermas import User_in_modify
from src.common.application.application_services import ApplicationService
from src.user.application.repositories.user_repository import User_repository


class Modify_manager_service(ApplicationService):

    def __init__(
        self,
        user_repository:User_repository,
    ):
        self.user_repository =user_repository

    async def execute(self, dto:Modify_manager_dto):
        if ( await self.user_repository.user_exists(dto.id)):
            if  (await self.user_repository.is_manager(dto.id)):
                user = User_in_modify(first_name=dto.first_name, last_name=dto.last_name, c_i=dto.c_i, 
                                      username = dto.username, email= dto.email, updated_at=datetime.now()
                                      )
                result = await self.user_repository.modify_client(dto.id,user)
                return result
            return {'code':400,'msg':'This user is not a manager'}       
        return {'code':400,'msg':'The Manager does not exist in the system'}       
        
        
        
        
             
