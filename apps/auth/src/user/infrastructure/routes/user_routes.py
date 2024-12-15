from fastapi import APIRouter, Depends

from src.user.application.services.modify_manager.modify_manager_service import Modify_manager_service
from src.user.application.services.modify_manager.types.modify_manager_dto import Modify_manager_dto
from src.user.infrastructure.routes.entries.modify_manager_entry import Modify_manager_entry
from src.user.application.services.find_managers.find_managers_service import Find_managers_service
from src.user.application.services.find_client.find_client_service import Find_client_service
from src.common.infrastructure.config.database.database import get_db
from src.user.application.services.modify_client.modify_client_service import Modify_client_service
from src.user.application.services.modify_client.types.modify_client_dto import Modify_client_dto
from src.user.infrastructure.repositories.user_postgres_repository import User_postgres_repository
from src.user.infrastructure.routes.entries.modify_client_entry import Modify_client_entry
from sqlalchemy.orm import Session

user_routes = APIRouter(
    prefix='/users',
    #tags=["user"]
)

@user_routes.patch('/client/:id',tags=['client'])   
async def modify_client(id:str, body: Modify_client_entry, session: Session = Depends(get_db)):
    
    dto = Modify_client_dto(id=id,first_name= body.first_name,last_name= body.last_name,
                       c_i= body.c_i, username= body.username, email= body.email)
    service = Modify_client_service(user_repository= User_postgres_repository(session))
    response = await service.execute(dto)
    return response


@user_routes.get('/client/:id',tags=['client'])
async def find_client(id: str, session: Session = Depends(get_db)):
    
    service = Find_client_service(user_repo= User_postgres_repository(session))
    response= await service.execute(id)
    return response


@user_routes.patch('/manager/:id',tags=['manager'])
async def modify_manager(id, body:Modify_manager_entry, session: Session = Depends(get_db)):
    dto = Modify_manager_dto(id=id,first_name= body.first_name,last_name= body.last_name,
                       c_i= body.c_i, username= body.username, email= body.email)
    service = Modify_manager_service(user_repository= User_postgres_repository(session))
    response = await service.execute(dto)
    return response
    return {'route':f'modify manager {id}'}


@user_routes.get('/manager/:id',tags=['manager'])
async def find_manager(id, session: Session = Depends(get_db)):
    service = Find_client_service(user_repo= User_postgres_repository(session))
    response= await service.execute(id)
    return response
    

@user_routes.get('/manager/all',tags=['manager'])
async def find_managers(session: Session = Depends(get_db)):
    service = Find_managers_service(user_repo= User_postgres_repository(session))
    response = await service.execute()
    return response




@user_routes.post('/superadmin/create', tags=['superadmin'])
def create_superadmin():
    return {'route': 'create superadmin'}
