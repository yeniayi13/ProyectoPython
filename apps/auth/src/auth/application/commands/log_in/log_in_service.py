from src.common.utils.result import Result
from src.common.application.ports.auth_handler import Auth_handler
from src.common.application.ports.hash_helper import Hash_helper
from src.user.application.repositories.user_repository import User_repository
from src.common.application.application_services import ApplicationService
from src.auth.application.commands.log_in.types.log_in_dto import Log_in_dto 
from src.auth.application.commands.log_in.types.log_in_response import Log_in_response
from src.common.utils.errors import Error

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


    
    async def execute(self,dto: Log_in_dto) -> Result[str] :
        if not(await self.user_repository.user_exists(dto.user)):
           return  Result.failure(Error('UserNotFound','This user does not exist in the system',404))
        
        
        response = await self.user_repository.find_user(dto.user)
       
        user =  response

        if(self.hash_helper.verify_password(dto.password, user.password)):
            token = self.auth_handler.sign(user.id, user.role)
            
            if token: return Result.success(token)
            
            return  Result.failure(Error('Internal Error','It was a problem while signing the token',500))  
        return Result.failure(Error('InvalidToken','Check your credentials',401))
        