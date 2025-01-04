from src.auth.application.commands.sign_up.types.sign_up_dto import Sign_up_dto 
from src.user.application.repositories.user_repository import User_repository
from src.user.application.schemas.user_schermas import User_in_create, User_in_response
from src.common.application.ports.event_handler import Event_handler
from src.common.application.ports.hash_helper import Hash_helper
from src.common.application.application_services import ApplicationService
from src.common.utils.result import Result
from src.common.utils.errors import Error
from uuid import uuid4
from datetime import datetime


class Sign_up_service(ApplicationService):


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


    
    async def execute(self,dto: Sign_up_dto)-> Result[User_in_response] :
        
        if (await self.user_repository.user_exists(dto.email)):
            return Result.failure(Error(name='EmailAlreadyInUse', msg='This email is already taken by a user', code=409)) 
        
        dto.password = self.hash_helper.get_password_hashed(dto.password)
        current_time = datetime.now() 
        user= User_in_create(id =str(uuid4()),first_name=dto.first_name,last_name= dto.last_name,
                             c_i=dto.c_i, username= dto.username,email=dto.email,password=dto.password,
                             role=dto.role.value, created_at= current_time, updated_at= current_time
                                 )
        
        
        new_user =  await self.user_repository.create_user(user)
        
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
            'first_name':new_user.first_name ,
            'last_name': new_user.last_name ,
            'C.I':new_user.c_i,
            'email':new_user.email
        }
        self.event_handler.publish(event,'users.client_created','users')
        print('Client created event published succesfully')
        
        return Result.success(response)   