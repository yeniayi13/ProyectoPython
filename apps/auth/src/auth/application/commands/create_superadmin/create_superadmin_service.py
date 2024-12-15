from datetime import datetime
from uuid import uuid4
from src.user.application.schemas.user_schermas import User_in_create
from src.auth.application.commands.create_superadmin.types.create_superadmin_dto import Create_superadmin_dto
from src.auth.application.commands.create_superadmin.types.create_superadmin_response import Create_superadmin_response
from src.common.application.ports.hash_helper import Hash_helper
from src.common.application.application_services import ApplicationService
from src.user.application.repositories.user_repository import User_repository



class Create_superadmin_service(ApplicationService):


    def __init__(
            self, 
            user_repository:User_repository, 
            hash_helper: Hash_helper,
    ):
        super().__init__()
        self.user_repository = user_repository
        self.hash_helper = hash_helper


    
    async def execute(self,dto: Create_superadmin_dto)-> Create_superadmin_response :
        dto.password = self.hash_helper.get_password_hashed(dto.password)
        current_time = datetime.now() 
        user= User_in_create(id =str(uuid4()),first_name=dto.first_name,last_name= dto.last_name,
                             c_i=dto.c_i, username= dto.username,email=dto.email,password=dto.password,
                             role=dto.role.value, created_at= current_time, updated_at= current_time
                                )
        if (await self.user_repository.user_exists(dto.email)):
            return {'code':409,'msg':'Email already associated to a SUPERADMIN'}
        response =  await self.user_repository.create_superadmin(user)
        #result = {
        #        'id' : response,
        #        'code': 201
        #        }
        return response   