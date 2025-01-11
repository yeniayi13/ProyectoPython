from pydantic import BaseModel
from src.common.infrastructure.config.database.postgres_base_repository import Base_repository
from src.common.utils.result import Result
from src.orders.application.repositories.client_repository import Client_repository
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_
from src.common.utils.errors import Error
from src.orders.application.schemas.client_schemas import Client_in_create
from src.orders.infrastructure.models.client import Client


class Client_postgres_repository(Base_repository,Client_repository):

    async def create_client(self, client:Client_in_create):
        try:
            new_client = Client(**client.model_dump( exclude_none=True ) )
            
            if not new_client:
                return Result.failure(Error('ClientNotCreated','A problem was found while creating a new Client',500))
            
            self.session.add(instance=new_client)
            self.session.commit()
            self.session.refresh(instance=new_client)

            return Result.success(new_client)
        except IntegrityError as e:
            if 'duplicate key value violates unique constraint "clients_c_i_key"' in str(e):
                return Result.failure(Error('CI_AlreadyInSystem','C.I already associated to a User',409))
            print(e)
            return Result.failure(Error('UnknownError','There is no clue about this error',500))  

    
    async def find_client(self, identification:str):
        try:
            print('id:',identification)
            client =  self.session.query(Client).filter(
                or_(
                    Client.email == identification,
                    Client.id == identification 
                )).first()
            return client
        except Exception as e:
            print(e)
        
    async def client_exists(self,id:str) -> bool:
        user =  await self.find_client(identification=id)
        #print('exist',bool(user))
        return bool(user)

    
    
    async def modify_client(self, id:str, client_in_modify: BaseModel):
        try:
            user = await self.find_client(id)
            attributes =[] 
            print('qu pasa vale',user)
            if not user:
                return Result.failure(Error('ClientNotFound','The client does not exist in the system',404))
            
            for key,value in client_in_modify.model_dump(exclude_none=True).items():
                 setattr(user,key,value)
                 if (key != 'updated_at'):
                    attributes.append(key)        
            
            self.session.commit()
            print('updatee')
            
            
            return Result.success(user)
        
        except IntegrityError as e:
            if 'duplicate key value violates unique constraint "clients_c_i_key"' in str(e):
                return Result.failure(Error('CI_AlreadyInSystem','C.I already associated to a client',409))
            if 'duplicate key value violates unique constraint "clients_username_key"' in str(e):
                return Result.failure(Error('UsernameAlreadyInSystem','Username already associated to a client',409))
            print('modify_client e:',e)
            return Result.failure(Error('UnknownError','There is no clue about this error',500))
            

    
    