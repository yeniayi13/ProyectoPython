from src.user.application.schemas.user_schermas import User_in_create, User_in_response
from src.user.application.repositories.user_repository import User_repository
from src.auth.application.commands.create_manager.types.create_manager_response import Create_manager_response
from src.auth.application.commands.create_manager.types.create_manager_dto import Create_manager_dto
from src.common.application.application_services import ApplicationService
from src.common.application.ports.event_handler import Event_handler
from src.common.application.ports.hash_helper import Hash_helper
from src.common.utils.errors import Error
from src.common.utils.result import Result
from datetime import datetime
from uuid import uuid4

class Create_manager_service(ApplicationService):


    def __init__(
            self, 
            user_repository:User_repository, 
            hash_helper: Hash_helper,
            event_handler: Event_handler
    ):
        super().__init__()
        self.user_repository = user_repository
        self.hash_helper = hash_helper
        self.event_handler = event_handler


    
    async def execute(self,dto: Create_manager_dto)-> Result[User_in_create]:
        dto.password = self.hash_helper.get_password_hashed(dto.password)
        current_time = datetime.now() 
        user= User_in_create(id =str(uuid4()),first_name=dto.first_name,last_name= dto.last_name,
                             c_i=dto.c_i, username= dto.username,email=dto.email,password=dto.password,
                             role=dto.role.value, created_at= current_time, updated_at= current_time
                                 )
        
        if (await self.user_repository.user_exists(dto.email)):
            return Result.failure(Error('ExistingEmail', 'Email already associated to a user', 409))
        
        new_user =  await self.user_repository.create_manager(user)

        if new_user.is_error():
            return new_user
        
        new_user = new_user.result()
        response = User_in_response(id= new_user.id, 
                            name= f'{new_user.first_name} {new_user.last_name}',
                            username= new_user.username,
                            c_i= new_user.c_i, email= new_user.email
                            )
        
        event = {
            'id':new_user.id,
            'name':f'{new_user.first_name} {new_user.last_name}' ,
            'C.I':new_user.c_i,
            'username':new_user.username
        }

        self.event_handler.publish(event,'users.manager_created','users')

        return Result.success(response)   
       