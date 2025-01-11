from src.common.application.application_services import ApplicationService
from src.common.utils.errors import Error
from src.common.utils.result import Result
from src.orders.application.repositories.client_repository import Client_repository
from src.orders.application.schemas.client_schemas import Client_in_update
from src.orders.application.services.listener_services.listeners_dtos.update_client_dto import  Update_client_dto

class Update_client_service(ApplicationService):
    def __init__(
            self,
            client_repository:Client_repository):
        
        super().__init__()
        self.client_repository = client_repository

    async def execute(self, dto:Update_client_dto) -> Result[bool]:
        if not (await self.client_repository.client_exists(dto.id)):
            return Result.failure(Error(name='ClientNotExist', msg='The client is being tried to update does not exist in the system', code=409)) 
        
        client= Client_in_update(
            first_name=dto.first_name,
            last_name= dto.last_name,
            c_i=dto.c_i, 
            email=dto.email
        )

        new_client =  await self.client_repository.modify_client(dto.id,client)

        if new_client.is_error():
            return new_client
        
        new_client = new_client.result()
        return Result.success(True)