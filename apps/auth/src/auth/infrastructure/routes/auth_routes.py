from src.common.utils.verify_role import verify_roles
from src.common.infrastructure.adapters.pika_event_handler import Pika_event_handler
from src.auth.application.commands.create_superadmin.types.create_superadmin_dto import Create_superadmin_dto
from src.auth.application.commands.create_superadmin.create_superadmin_service import Create_superadmin_service
from src.auth.application.commands.create_manager.types.create_manager_dto import Create_manager_dto
from src.auth.application.commands.create_manager.create_manager_service import Create_manager_service
from src.auth.application.commands.sign_up.types.sign_up_dto import Sign_up_dto
from src.auth.application.commands.sign_up.sign_up_service import Sign_up_service
from src.auth.application.commands.log_in.log_in_service import Log_in_service
from src.auth.application.commands.log_in.types.log_in_dto import Log_in_dto
from src.auth.infrastructure.routes.entries.create_manager_dto import Create_manager_entry
from src.auth.infrastructure.routes.entries.create_superadmin_entry import Create_superadmin_entry
from src.auth.infrastructure.routes.entries.sign_up_dto import Sign_up_dto as sign_up_entry
from src.auth.infrastructure.routes.entries.log_in_dto import Log_in_dto as log_in_entry
from src.user.application.schemas.user_schermas import User_in_response
from src.user.application.models.user import Roles
from src.user.infrastructure.repositories.user_postgres_repository import User_postgres_repository
from src.common.application.application_services import ApplicationService
from src.common.infrastructure.adapters.JWT_auth_handler import JWT_auth_handler
from src.common.infrastructure.adapters.bcrypt_hash_helper import Bcrypt_hash_helper
from src.common.infrastructure.config.event_handler.event_handler_connection import get_channel
from src.common.infrastructure.config.database.database import get_db
from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm 
from sqlalchemy.orm import Session
from pika.adapters.blocking_connection import BlockingChannel

auth_router = APIRouter(
    prefix='/auth',
    tags=["auth"]
)

auth = JWT_auth_handler()

@auth_router.post('/sign_up', status_code=201,responses={
        409: {"description": "DB consitency error"},
        201: {"description": "Client Created"},
        500: {"description": "Internal Server Eror"}
    })
async def sign_up(entry:sign_up_entry, response:Response, session: Session = Depends(get_db), channel:BlockingChannel = Depends(get_channel) ):
    role = Roles.CLIENT
    dto = Sign_up_dto(first_name=entry.first_name, last_name=entry.last_name, c_i=entry.c_i, 
                username=entry.username,email=entry.email, password=entry.password, role=role)
    
    service:ApplicationService = Sign_up_service( 
        user_repository = User_postgres_repository(session),
        hash_helper=Bcrypt_hash_helper(),
        event_handler=Pika_event_handler(channel=channel)
        )
    result = await service.execute(dto)

    if result.is_error():
        response.status_code = result.error.code
        return {'msg': result.get_error_message() }
        
    return result.result()





@auth_router.post('/log_in',status_code=200)
async def log_in(response:Response, session: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends() ):
    dto =Log_in_dto(user= form_data.username, password = form_data.password)
    
    service = Log_in_service(
        user_repository = User_postgres_repository(session), 
        hash_helper=Bcrypt_hash_helper(),
        auth_handler=JWT_auth_handler())
    
    result = await service.execute(dto)
    
    if result.is_error():
        response.status_code = result.error.code
        return {'msg': result.get_error_message() }
    
    
    return {
        "access_token": result.result(),
        "token_type": "bearer"
        }





@auth_router.post('/create_manager', status_code=201,responses={
        409: {"description": "DB consitency error"},
        201: {"description": "Manager Created"},
        500: {"description": "Internal Server Eror"}
    })
async def create_manager(entry:Create_manager_entry, response:Response, info = Depends(auth.decode), session: Session = Depends(get_db), channel:BlockingChannel = Depends(get_channel)):
    
    if info.is_error():
        response.status_code = info.error.code
        return {'msg': info.get_error_message()}
    
    role = info.result()
    print(role)

    if not verify_roles(role['role'],['SUPERADMIN']):
        response.status_code = 401
        return {'msg': 'This information is not accesible for this user' }
    
    role = Roles.MANAGER
    dto = Create_manager_dto(first_name=entry.first_name, last_name=entry.last_name, c_i=entry.c_i, 
                username=entry.username,email=entry.email, password=entry.password, role=role)
    
    service:ApplicationService = Create_manager_service( 
        user_repository = User_postgres_repository(session),
        hash_helper=Bcrypt_hash_helper(),
        event_handler=Pika_event_handler(channel=channel))
    result = await service.execute(dto)
    
    if result.is_error():
        response.status_code = result.error.code
        return {'msg': result.get_error_message() }
    
    return result.result()





@auth_router.post('/create_superadmin', status_code=201, responses={
        409: {"description": "DB consitency error"},
        201: {"description": "SuperAdmin Created"},
        500: {"description": "Internal Server Eror"}
    })
async def create_superadmin(entry:Create_superadmin_entry, response:Response, info = Depends(auth.decode), session: Session = Depends(get_db), channel:BlockingChannel = Depends(get_channel)):
    if info.is_error():
        response.status_code = info.error.code
        return {'msg': info.get_error_message()}
    
    role = info.result()
    print(role)

    if not verify_roles(role['role'],['SUPERADMIN']):
        response.status_code = 401
        return {'msg': 'This information is not accesible for this user' }
    
    role = Roles.SUPERADMIN
    dto = Create_superadmin_dto(first_name=entry.first_name, last_name=entry.last_name, c_i=entry.c_i, 
                username=entry.username,email=entry.email, password=entry.password, role=role)
    
    service:ApplicationService = Create_superadmin_service( 
        user_repository = User_postgres_repository(session),
        hash_helper=Bcrypt_hash_helper(),
        event_handler=Pika_event_handler(channel=channel))
    result = await service.execute(dto)
    
    if result.is_error():
        response.status_code = result.error.code
        return {'msg': result.get_error_message() }    
    return result.result()