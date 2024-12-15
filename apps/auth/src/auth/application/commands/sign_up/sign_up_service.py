from src.user.application.schemas.user_schermas import User_in_create
from src.common.application.ports.hash_helper import Hash_helper
from src.common.application.application_services import ApplicationService
from src.auth.application.commands.sign_up.types.sign_up_dto import Sign_up_dto 
from src.auth.application.commands.sign_up.types.sign_up_response import Sign_up_response
from src.user.application.repositories.user_repository import User_repository
from uuid import uuid4
from datetime import datetime


class Sign_up_service(ApplicationService):


    def __init__(
            self, 
            user_repository:User_repository, 
            hash_helper: Hash_helper,
    ):
        super().__init__()
        self.user_repository = user_repository
        self.hash_helper = hash_helper


    
    async def execute(self,dto: Sign_up_dto)-> Sign_up_response :
        dto.password = self.hash_helper.get_password_hashed(dto.password)
        current_time = datetime.now() 
        user= User_in_create(id =str(uuid4()),first_name=dto.first_name,last_name= dto.last_name,
                             c_i=dto.c_i, username= dto.username,email=dto.email,password=dto.password,
                             role=dto.role.value, created_at= current_time, updated_at= current_time
                                 )
        if (await self.user_repository.user_exists(dto.email)):
            return {'code':409,'msg':'Email already associated with a user'}
        response =  await self.user_repository.create_user(user)
        return response   
    

     #result = {
        #        'id' : response,
        #        'code': 201
        #        }