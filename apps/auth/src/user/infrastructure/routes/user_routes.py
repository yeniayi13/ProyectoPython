from src.user.application.services.find_me.find_me_service import Find_me_service
from src.user.application.services.modify_manager.modify_manager_service import Modify_manager_service
from src.user.application.services.modify_manager.types.modify_manager_dto import Modify_manager_dto
from src.user.application.services.modify_client.modify_client_service import Modify_client_service
from src.user.application.services.modify_client.types.modify_client_dto import Modify_client_dto
from src.user.application.services.find_managers.find_managers_service import Find_managers_service
from src.user.application.services.find_client.find_client_service import Find_client_service
from src.user.infrastructure.routes.entries.modify_client_entry import Modify_client_entry
from src.user.infrastructure.routes.entries.modify_manager_entry import Modify_manager_entry
from src.user.infrastructure.repositories.user_postgres_repository import User_postgres_repository
from src.common.infrastructure.adapters.pika_event_handler import Pika_event_handler
from src.common.infrastructure.config.event_handler.event_handler_connection import get_channel
from src.common.utils.verify_role import verify_roles
from src.common.infrastructure.adapters.JWT_auth_handler import JWT_auth_handler
from src.common.infrastructure.config.database.database import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordBearer
from pika.adapters.blocking_connection import BlockingChannel

user_routes = APIRouter(
    prefix='/users',
    #tags=["user"]
)

auth = JWT_auth_handler()


@user_routes.patch('/client/:id',tags=['client'])   
async def modify_client(id:str, 
                        response:Response, 
                        body: Modify_client_entry, 
                        info = Depends(auth.decode),
                        session: Session = Depends(get_db),
                        channel:BlockingChannel = Depends(get_channel)
                        ):
    
    if info.is_error():
        response.status_code = info.error.code
        return {'msg': info.get_error_message()}
    
    role = info.result()

    if not verify_roles(role['role'],['SUPERADMIN', 'CLIENT']):
        response.status_code = 401
        return {'msg': 'This information is not accesible for this user' }
    
    dto = Modify_client_dto(id=id,first_name= body.first_name,last_name= body.last_name,
                       c_i= body.c_i, username= body.username, email= body.email)
    service = Modify_client_service(
        user_repository= User_postgres_repository(session),
        event_handler=Pika_event_handler(channel=channel)
        )
    result = await service.execute(dto)

    if result.is_error():
        response.status_code = result.error.code
        return {'msg': result.get_error_message() } 
    return result.result()





@user_routes.get('/client/:id',tags=['client'])
async def find_client(id: str, response:Response, info = Depends(auth.decode),session: Session = Depends(get_db)):
    if info.is_error():
        response.status_code = info.error.code
        return {'msg': info.get_error_message()}
    
    role = info.result()

    if not verify_roles(role['role'],['SUPERADMIN']):
        response.status_code = 401
        return {'msg': 'This information is not accesible for this user' }
    
    service = Find_client_service(user_repo= User_postgres_repository(session))
    result= await service.execute(id)
    
    if result.is_error():
        response.status_code = result.error.code
        return {'msg': result.get_error_message() } 
    return result.result()





@user_routes.patch('/manager/:id',tags=['manager'])
async def modify_manager(id:str, 
                         body:Modify_manager_entry, 
                         response:Response, 
                         info = Depends(auth.decode),
                         session: Session = Depends(get_db),
                         channel:BlockingChannel = Depends(get_channel)):
    if info.is_error():
        response.status_code = info.error.code
        return {'msg': info.get_error_message()}
    
    role = info.result()

    if not verify_roles(role['role'],['SUPERADMIN']):
        response.status_code = 401
        return {'msg': 'This information is not accesible for this user' }
    
    dto = Modify_manager_dto(id=id,first_name= body.first_name,last_name= body.last_name,
                       c_i= body.c_i, username= body.username, email= body.email)
    
    service = Modify_manager_service(
        user_repository= User_postgres_repository(session),
        event_handler= Pika_event_handler(channel=channel))
    result = await service.execute(dto)
    
    if result.is_error():
        response.status_code = result.error.code
        return {'msg': result.get_error_message() } 
    return result.result()





@user_routes.get('/manager/:id',tags=['manager'])
async def find_manager(id:str, response:Response, info = Depends(auth.decode),session: Session = Depends(get_db)):
    if info.is_error():
        response.status_code = info.error.code
        return {'msg': info.get_error_message()}
    
    role = info.result()


    if not verify_roles(role['role'],['SUPERADMIN']):
        response.status_code = 401
        return {'msg': 'This information is not accesible for this user' }
    

    service = Find_client_service(user_repo= User_postgres_repository(session))
    result= await service.execute(id)
    
    if result.is_error():
        response.status_code = result.error.code
        return {'msg': result.get_error_message() } 
    return result.result()
    




@user_routes.get('/manager/all',tags=['manager'])
async def find_managers(response:Response, info = Depends(auth.decode),  session: Session = Depends(get_db)):
    
    if info.is_error():
        response.status_code = info.error.code
        return {'msg': info.get_error_message()}
    
    role = info.result()

    if not verify_roles(role['role'],['SUPERADMIN']):
        response.status_code = 401
        return {'msg': 'This information is not accesible for this user' }   
        
    service = Find_managers_service(user_repo= User_postgres_repository(session))
    
    result = await service.execute()
    

    if result.is_error():
        response.status_code = result.error.code
        return {'msg': result.get_error_message() } 
    return result.result()





@user_routes.get('/client/me',tags=['client'])
async def find_me(response:Response, info = Depends(auth.decode),session: Session = Depends(get_db)):
    if info.is_error():
        response.status_code = info.error.code
        return {'msg': info.get_error_message()}
    
    role = info.result()
    print(role)

    if not verify_roles(role['role'],['SUPERADMIN','CLIENT','MANAGER']):
        response.status_code = 401
        return {'msg': 'This information is not accesible for this user' }
    
    service = Find_me_service(user_repo= User_postgres_repository(session))
    result= await service.execute(role['user_id'])
    
    if result.is_error():
        response.status_code = result.error.code
        return {'msg': result.get_error_message() } 
    return result.result()
