from src.common.application.application_services import ApplicationService
from src.common.utils.errors import Error
from src.common.utils.result import Result
from src.orders.application.repositories.client_repository import Client_repository
from src.orders.application.schemas.client_schemas import Client_in_create
from src.orders.application.services.listener_services.listeners_dtos.create_client_dto import Create_client_dto

class Create_client_service(ApplicationService):
    def __init__(
            self,
            client_repository:Client_repository):
        
        super().__init__()
        self.client_repository = client_repository

    async def execute(self,dto:Create_client_dto) -> Result[bool]:
        if (await self.client_repository.client_exists(dto.id)):
            return Result.failure(Error(name='UserAlreadyExists', msg='This user is already in the system', code=409)) 
        
        
        client= Client_in_create(
            id =dto.id,
            first_name=dto.first_name,
            last_name= dto.last_name,
            c_i=dto.c_i, 
            email=dto.email
        )
        
        
        new_client =  await self.client_repository.create_client(client)
        
        if new_client.is_error():
            return new_client
        
        new_client = new_client.result()
        return Result.success(True)