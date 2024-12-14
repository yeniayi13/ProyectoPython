from src.common.application.ports.auth_handler import Auth_handler
from src.common.application.ports.hash_helper import Hash_helper
from src.user.application.repositories.user_repository import User_repository
from src.common.application.application_services import ApplicationService
from src.auth.application.commands.log_in.types.log_in_dto import Log_in_dto 
from src.auth.application.commands.log_in.types.log_in_response import Log_in_response

class Log_in_service[log_in_dto,log_in_response](ApplicationService):
    
    def __init__(
            self,
            user_repository:User_repository, 
            hash_helper: Hash_helper,
            auth_handler:Auth_handler
    ):
        super().__init__()
        self.user_repository = user_repository
        self.hash_helper = hash_helper
        self.auth_handler = auth_handler


    
    async def execute(self,dto: Log_in_dto) -> Log_in_response :
        if not(await self.user_repository.user_exists(dto.user)):
           return {'code':409,'msg':'This user does not exist'}
        
        
        user = await self.user_repository.find_user(dto.user)

        if(self.hash_helper.verify_password(dto.password, user.password)):
            token = self.auth_handler.sign(user.id, user.role)
            
            if token: return token
            
            return {
            'code':500,
            "error": "Internal Error",
            "error_description": "It was a problem while signing the token"
            } 
        return {
            'code':401,
            "error": "invalid_token",
            "error_description": "Check your credentials"
            }
        