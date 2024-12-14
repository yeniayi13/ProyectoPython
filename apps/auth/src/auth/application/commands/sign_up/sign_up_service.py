from uuid import uuid4
from src.common.application.ports.hash_helper import Hash_helper
from src.common.application.application_services import ApplicationService
from src.auth.application.commands.sign_up.types.sign_up_dto import Sign_up_dto 
from src.auth.application.commands.sign_up.types.sign_up_response import Sign_up_response
from src.user.application.repositories.user_repository import User_repository



class Sign_up_service[Sign_up_dto,Sign_up_response](ApplicationService):


    def __init__(
            self, 
            user_repository:User_repository, 
            hash_helper: Hash_helper,
    ):
        super().__init__()
        self.user_repository = user_repository
        self.hash_helper = hash_helper


    
    async def execute(self,dto: Sign_up_dto)-> Sign_up_response :
        dto.id = str(uuid4())
        dto.password = self.hash_helper.get_password_hashed(dto.password)
        if (await self.user_repository.user_exists(dto.email)):
            return {'code':409,'msg':'Email already associated to a user'}
        response =  await self.user_repository.create_user(dto)
        #result = {
        #        'id' : response,
        #        'code': 201
        #        }
        return response   