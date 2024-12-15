from fastapi import APIRouter, Depends

from src.common.infrastructure.config.database.database import get_db
from src.user.application.services.modify_client_service import Modify_client_service
from src.user.application.services.types.modify_client_dto import Modify_client_dto
from src.user.infrastructure.repositories.user_postgres_repository import User_postgres_repository
from src.user.infrastructure.routes.entries.modify_client_entry import Modify_client_entry
from sqlalchemy.orm import Session

user_routes = APIRouter(
    prefix='/users',
    #tags=["user"]
)


@user_routes.delete('/client/:id', tags=['client'])
def delete_client(id):
    return {'route': f'delete client  {id}'}


@user_routes.patch('/client/:id',tags=['client'])   
async def modify_client(id:str, body: Modify_client_entry, session: Session = Depends(get_db)):
    #print(body)
    
    dto = Modify_client_dto(id=id,first_name= body.first_name,last_name= body.last_name,
                       c_i= body.c_i, username= body.username, email= body.email)
    service = Modify_client_service(user_repository= User_postgres_repository(session))
    response = await service.execute(dto)
    return response
    
    #body2 = body.model_dump(exclude_unset=True)
    #print(body)
    #body2['id'] = id
    #return {'body':body2 }


@user_routes.get('/client/:id',tags=['client'])
def find_client(id):
    return {'route': f'find client {id}'}

@user_routes.post('/client/create', tags=['client'])
def create_client():
    return {'route': 'create_client'}









@user_routes.delete('/manager/:id', tags=['manager'])
def delete_manager(id):
    return {'route': f'delete manager {id}'}

@user_routes.put('/manager/:id',tags=['manager'])
def modify_manager(id):
    return {'route':f'modify manager {id}'}


@user_routes.get('/manager/:id',tags=['manager'])
def find_manager(id):
    return {'route':f'find manager {id}'}

@user_routes.get('/manager/all',tags=['manager'])
def find_managers():
    return {'route':f'find manager all'}




@user_routes.post('/superadmin/create', tags=['superadmin'])
def create_superadmin():
    return {'route': 'create superadmin'}
