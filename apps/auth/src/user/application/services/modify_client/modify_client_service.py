from src.user.application.schemas.user_schermas import User_in_modify, User_in_response
from src.user.application.repositories.user_repository import User_repository
from src.user.application.services.modify_client.types.modify_client_dto import Modify_client_dto
from src.common.application.ports.event_handler import Event_handler
from src.common.utils.result import Result
from src.common.application.application_services import ApplicationService
from src.common.utils.errors import Error
from datetime import datetime

class Modify_client_service(ApplicationService):

    def __init__(
        self,
        user_repository:User_repository,
        event_handler: Event_handler,

    ):
        self.user_repository =user_repository
        self.event_handler = event_handler
        

    async def execute(self, dto:Modify_client_dto):
        if  ( await self.user_repository.user_exists(dto.id)):
            user = User_in_modify(first_name=dto.first_name, last_name=dto.last_name, c_i=dto.c_i, 
                                 username = dto.username, email= dto.email, updated_at=datetime.now()
                                 )
            modified_user = await self.user_repository.modify_client(dto.id,user)
            if modified_user.is_error():
                    return modified_user
                   
            modified_user = modified_user.result()
            response = User_in_response(id= modified_user.id, 
                                    name= f'{modified_user.first_name} {modified_user.last_name}',
                                    username= modified_user.username,
                                    c_i= modified_user.c_i, email= modified_user.email
                                    )
            
            event = {
            'id':modified_user.id,
            'name':f'{modified_user.first_name} {modified_user.last_name}' ,
            'C.I':modified_user.c_i,
            'username':modified_user.username
            }

            self.event_handler.publish(event,'users.client_modified','users')

            return Result.success(response)
        return Result.failure(Error('ClientNotExist','The user does not exist in the system',400))
        
        
             
